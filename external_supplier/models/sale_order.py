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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_sync_price_and_stock(self):
        for line in self.order_line.filtered(lambda x: x.external_supplier_id):
            line.external_supplier_id.update_order_lines_price_and_stock(line)

    def action_confirm(self):
        """
            BHC OVERRIDE : ADD CONTEXT
        """
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        # <BHC OVERRIDE>  add context to retrieve in stock.rule
        context['product_supplier_mapping'] = {}
        for line in self.order_line:
            context['product_supplier_mapping'].setdefault(line.product_id.id, [])
            context['product_supplier_mapping'][line.product_id.id].append({
                'supplier_id': line.external_supplier_id.id,
                'quantity': line.product_uom_qty
            })
        # </BHC OVERRIDE>
        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock_supplier = fields.Char(string='Supplier stock',
                                 help="Legend of the function price and avalability\nBlue = stock decreases\nRed = price of the supplier increases\nGreen =price of the supplier decreases")

    external_supplier_id = fields.Many2one('external.supplier', string="External supplier", required=False)
    price_and_stock_state = fields.Selection([
        ('price_decreased', "Price has decreased"),
        ('price_increased', "Price has increased"),
        ('out_of_stock', 'Product is out of stock')
    ], string='price and stock state')

    @api.onchange('product_id')
    def auto_set_supplier(self):
        if self.product_id and self.product_id.seller_ids:
            supplier = self.product_id.seller_ids[0].name
            external_supplier = self.env['external.supplier'].search([
                ('supplier_id', '=', supplier.id)
            ])
            self.write({"external_supplier_id": external_supplier})
            return {
                'domain': {
                    'external_supplier_id': [
                        ('supplier_id', 'in', self.product_id.mapped('seller_ids.name').ids)
                    ]
                }
            }
