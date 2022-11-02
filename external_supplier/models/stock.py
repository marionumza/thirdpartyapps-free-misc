######################################################################################################
#
# Copyright © B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# This code is subject to the BHC License Agreement
# Please see the License.txt file for more information
# All other rights reserved
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
######################################################################################################

import logging
from collections import defaultdict

import time
from dateutil.relativedelta import relativedelta
from itertools import groupby

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_rule import ProcurementException

_logger = logging.getLogger(__name__)


class OrderHistory(models.Model):
    _name = "external.supplier.order_history"
    _description = "Order history entry from external supplier"

    name = fields.Char(string='Name')
    expected_date = fields.Date(string="Expected Date")
    update_date = fields.Date(string="Updated date")
    description = fields.Char(string='Description')
    stock_picking_id = fields.Many2one("stock.picking", string="Transfer")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_date = fields.Date(string="Delivery date", help="Delivery date")
    history_line = fields.One2many('external.supplier.order_history', 'stock_picking_id', string="idLabel")
    external_supplier_id = fields.Many2one('external.supplier', string="External supplier", compute='_compute_external_supplier_id')

    @api.depends('partner_id')
    def _compute_external_supplier_id(self):
        for record in self:
            record.external_supplier_id = self.env['external.supplier'].search(
                [('supplier_id', '=', self.partner_id.id)], limit=1)

    def action_update_status(self):
        self.ensure_one()
        if not self.external_supplier_id:
            raise UserError(_("The supplier of this picking is not linked to an external supplier."))
        if not self.origin:
            raise UserError(_("This picking is not linked to a purchase nor a sale."))
        self.external_supplier_id.get_order_status_from_external_supplier(self)

    def handle_status_update(self, date, description):
        self.ensure_one()
        today = time.strftime('%Y-%m-%d')
        history_command = self.env['external.supplier.order_history'].search([
            ('stock_picking_id', '=', self.id),
            ('description', '=', description)
        ])
        if not history_command:
            history_command = self.env['external.supplier.order_history'].create({
                'stock_picking_id': self.id,
                'description': description,
                'expected_date': date,
                'update_date': today
            })
        else:
            history_command.write({'expected_date': date, 'update_date': today})
        return history_command


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_buy(self, procurements):
        """
            OVERRIDE BHC
            add the supplier corresponding to the one you choose in sales and not the one that is the cheapest
        """
        procurements_by_po_domain = defaultdict(list)
        errors = []
        for procurement, rule in procurements:

            # Get the schedule date in order to find a valid seller
            procurement_date_planned = fields.Datetime.from_string(procurement.values['date_planned'])
            schedule_date = (procurement_date_planned - relativedelta(days=procurement.company_id.po_lead))
            supplier = False

            # <BHC OVERRIDE>
            # retrieve the sale order line and get the good supplier
            if self.env.context.get('product_supplier_mapping'):
                product_suppliers = self.env.context['product_supplier_mapping'][procurement.product_id.id]
            else:
                product_suppliers = []

            product_supplier_id = None
            for index, product_supplier in enumerate(product_suppliers):
                if product_supplier['quantity'] == procurement.product_qty:
                    product_supplier_id = product_supplier['supplier_id']
                    product_suppliers.pop(index)
                    break

            supplier_external = self.env['external.supplier'].browse(product_supplier_id) if product_supplier_id else None
            if supplier_external:
                supplier = self.env['product.supplierinfo'].search([
                    ('name', '=', supplier_external.supplier_id.id),
                    ('product_id', '=', procurement.product_id.id)
                ])
            else:
                # BHC OVERRIDE
                # following lines are vanilla but the fact that they are in an else statement is an override
                if procurement.values.get('supplierinfo_id'):
                    supplier = procurement.values['supplierinfo_id']
                else:
                    supplier = procurement.product_id.with_company(procurement.company_id.id)._select_seller(
                        partner_id=procurement.values.get("supplierinfo_name"),
                        quantity=procurement.product_qty,
                        date=schedule_date.date(),
                        uom_id=procurement.product_uom)

                # Fall back on a supplier for which no price may be defined. Not ideal, but better than
                # blocking the user.
                supplier = supplier or procurement.product_id._prepare_sellers(False).filtered(
                    lambda s: not s.company_id or s.company_id == procurement.company_id
                )[:1]

                if not supplier:
                    msg = _('There is no matching vendor price to generate the purchase order for product %s (no vendor defined, minimum quantity not reached, dates not valid, ...). Go on the product form and complete the list of vendors.') % (procurement.product_id.display_name)
                    errors.append((procurement, msg))
            # </BHC OVERRIDE>

            partner = supplier.name
            # we put `supplier_info` in values for extensibility purposes
            procurement.values['supplier'] = supplier
            procurement.values['propagate_cancel'] = rule.propagate_cancel

            domain = rule._make_po_get_domain(procurement.company_id, procurement.values, partner)
            procurements_by_po_domain[domain].append((procurement, rule))

        if errors:
            raise ProcurementException(errors)

        for domain, procurements_rules in procurements_by_po_domain.items():
            # Get the procurements for the current domain.
            # Get the rules for the current domain. Their only use is to create
            # the PO if it does not exist.
            procurements, rules = zip(*procurements_rules)

            # Get the set of procurement origin for the current domain.
            origins = set([p.origin for p in procurements])
            # Check if a PO exists for the current domain.
            po = self.env['purchase.order'].sudo().search([dom for dom in domain], limit=1)
            company_id = procurements[0].company_id
            if not po:
                # We need a rule to generate the PO. However the rule generated
                # the same domain for PO and the _prepare_purchase_order method
                # should only uses the common rules's fields.
                vals = rules[0]._prepare_purchase_order(company_id, origins, [p.values for p in procurements])
                # The company_id is the same for all procurements since
                # _make_po_get_domain add the company in the domain.
                # We use SUPERUSER_ID since we don't want the current user to be follower of the PO.
                # Indeed, the current user may be a user without access to Purchase, or even be a portal user.
                po = self.env['purchase.order'].with_company(company_id).with_user(SUPERUSER_ID).create(vals)
            else:
                # If a purchase order is found, adapt its `origin` field.
                if po.origin:
                    missing_origins = origins - set(po.origin.split(', '))
                    if missing_origins:
                        po.write({'origin': po.origin + ', ' + ', '.join(missing_origins)})
                else:
                    po.write({'origin': ', '.join(origins)})

            procurements_to_merge = self._get_procurements_to_merge(procurements)
            procurements = self._merge_procurements(procurements_to_merge)

            po_lines_by_product = {}
            grouped_po_lines = groupby(po.order_line.filtered(lambda l: not l.display_type and l.product_uom == l.product_id.uom_po_id).sorted(lambda l: l.product_id.id), key=lambda l: l.product_id.id)
            for product, po_lines in grouped_po_lines:
                po_lines_by_product[product] = self.env['purchase.order.line'].concat(*list(po_lines))
            po_line_values = []
            for procurement in procurements:
                po_lines = po_lines_by_product.get(procurement.product_id.id, self.env['purchase.order.line'])
                po_line = po_lines._find_candidate(*procurement)

                if po_line:
                    # If the procurement can be merge in an existing line. Directly
                    # write the new values on it.
                    vals = self._update_purchase_order_line(procurement.product_id,
                        procurement.product_qty, procurement.product_uom, company_id,
                        procurement.values, po_line)
                    po_line.write(vals)
                else:
                    # If it does not exist a PO line for current procurement.
                    # Generate the create values for it and add it to a list in
                    # order to create it in batch.
                    partner = procurement.values['supplier'].name
                    po_line_values.append(self.env['purchase.order.line']._prepare_purchase_order_line_from_procurement(
                        procurement.product_id, procurement.product_qty,
                        procurement.product_uom, procurement.company_id,
                        procurement.values, po))
            self.env['purchase.order.line'].sudo().create(po_line_values)
