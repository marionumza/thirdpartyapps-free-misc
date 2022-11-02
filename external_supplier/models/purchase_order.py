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

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_external_supplier = fields.Many2one('external.supplier', compute='_compute_vendor_supplier', store=True)
    vendor_supplier_type = fields.Selection(related="vendor_external_supplier.supplier_type")
    order_date = fields.Char(string="order date")
    external_supplier_order_date = fields.Date(string="External supplier order date")
    sent_to_external_supplier = fields.Boolean(string='Order send', copy=False)
    send_automatically_to_supplier = fields.Boolean(string='Send to external supplier', default=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self._compute_vendor_supplier()
        for record in self:
            record.send_automatically_to_supplier = bool(record.vendor_external_supplier)

    @api.depends('partner_id')
    def _compute_vendor_supplier(self):
        for record in self:
            external_supplier = self.env['external.supplier'].search([('supplier_id', '=', record.partner_id.id)],
                                                                     limit=1)
            record.vendor_external_supplier = external_supplier.id if external_supplier else False

    def button_confirm(self):
        """
        OVERRIDE BHC to send order to supplier before confirmation so that if sending fails, then it's not confirmed.
        """
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # <BHC OVERRIDE>
            if order.vendor_external_supplier and order.send_automatically_to_supplier:
                order._send_to_supplier()
            # </BHC OVERRIDE>
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True

    def action_sync_price_and_stock(self):
        if not self.vendor_external_supplier:
            raise UserError(_('This supplier is not supported !'))
        self.vendor_external_supplier.update_order_lines_price_and_stock(self.order_line)

    def _send_to_supplier(self):
        if self.sent_to_external_supplier:
            raise UserError(_('Information: Already send order'))
        self.vendor_external_supplier.send_order_to_external_supplier(self)
        self.sent_to_external_supplier = True
        self._notify_order_sent_to_external_supplier()

    def _notify_order_sent_to_external_supplier(self):
        self.ensure_one()
        self.message_post(body=_("Order has been sent to external supplier with success."))


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    external_supplier_id = fields.Many2one('external.supplier', related="order_id.vendor_external_supplier")
    stock_supplier = fields.Char(string='Supplier stock',
                                 help="Legend of the function price and availability\nBlue = stock decreases\nRed = price of the supplier increases\nGreen =price of the supplier decreases")
    price_and_stock_state = fields.Selection([
        ('price_decreased', "Price has decreased"),
        ('price_increased', "Price has increased"),
        ('out_of_stock', 'Product is out of stock')
    ], string='price and stock state')
