# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt. Ltd. <www.botspotinfoware.com>
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
from datetime import datetime, date, time, timedelta
from odoo import models, fields, api, exceptions, _, SUPERUSER_ID

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_saving = fields.Float(string="Total Savings", compute="_compute_total_order_saving")

    @api.depends('order_line')
    def _compute_total_order_saving(self):
        for record in self:
            if record.order_line:
                temp_total_saving = 0.00
                for line in record.order_line:
                    if line.product_id and line.unit_saving and line.unit_saving > 0.00:
                        temp_total_saving += line.unit_saving * line.product_uom_qty
                record.total_saving = temp_total_saving
            else:
                record.total_saving = 0.00


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    our_price = fields.Float(string="Our Unit Price", compute="_compute_line_our_price_and_unit_saving")
    unit_saving = fields.Float(string="Unit Saving", compute="_compute_line_our_price_and_unit_saving")

    @api.depends('product_id')
    def _compute_line_our_price_and_unit_saving(self):
        for record in self:
            if record.product_id:
                if record.product_id.our_price and record.product_id.total_saving:
                    record.our_price = record.product_id.our_price
                    record.unit_saving = record.product_id.total_saving
                else:
                    record.our_price = 0.00
                    record.unit_saving = 0.00
            else:
                record.our_price = 0.00
                record.unit_saving = 0.00

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            if line.our_price > 0.00:
                price = line.our_price * (1 - (line.discount or 0.0) / 100.0)
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    #### Condition for 'Our_price' and 'Normal Price' ####
    #def _get_display_price(self, product):
    '''    # TO DO: move me in master/saas-16 on sale.order
        # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
        # to be able to compute the full price

        # it is possible that a no_variant attribute is still in a variant if
        # the type of the attribute has been changed after creation.
        no_variant_attributes_price_extra = [
            ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                lambda ptav:
                    ptav.price_extra and
                    ptav not in product.product_template_attribute_value_ids
            )
        ]
        if no_variant_attributes_price_extra:
            product = product.with_context(
                no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
            )

        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            #### Condition for 'Our_price' and 'Normal Price'
            if product.with_context(pricelist=self.order_id.pricelist_id.id).our_price and product.with_context(pricelist=self.order_id.pricelist_id.id).total_saving:
                return product.with_context(pricelist=self.order_id.pricelist_id.id).our_price
            else:
                return product.with_context(pricelist=self.order_id.pricelist_id.id).price

        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        if currency != self.order_id.pricelist_id.currency_id:
            base_price = currency._convert(
                base_price, self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)'''

