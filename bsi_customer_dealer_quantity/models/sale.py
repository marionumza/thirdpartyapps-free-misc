# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt ltd'<www.botspotinfoware.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dealer_minimum_quantity = fields.Float(string="Dealer Min Qty", default='1')

    # It will works on products whenever customer is dealer and set product's dealer price then dealer price is add in unit price otherwise customer is not dealer then list price is add in unit price
    @api.onchange('product_id')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        for line in self:
            if line.order_partner_id.is_dealer and line.product_id.dealer_price:
                line.price_unit = self.product_id.dealer_price
            else:
                line.price_unit = self.product_id.lst_price
        return res

    # This constrains functionality is e.g whenever customer is dealer then dealer minimum quantity less then quantity otherwise is not then validation error raises 
    @api.constrains('product_uom_qty')
    def valid_quantity(self):
        for record in self:
            if record.order_partner_id.is_dealer:
                if record.product_uom_qty < record.product_id.dealer_minimum_quantity:
                    raise ValidationError("Your order quantity is not enough as a dealer")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # When customer is dealer then unit price and quantity is change on order
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            if record.partner_id and record.partner_id.is_dealer:
                if record.order_line:
                    for line in record.order_line:
                        line.price_unit = line.product_id.dealer_price
                        line.product_uom_qty = line.product_id.dealer_minimum_quantity
