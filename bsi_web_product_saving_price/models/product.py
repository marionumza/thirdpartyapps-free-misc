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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    our_price_deduct = fields.Float('Variant Deduct Price', compute='_compute_product_our_price_deduct', help="This is the sum of the our deduct price of all attributes")
    our_price = fields.Float(string="Our Price", compute="_compute_product_our_price")
    total_saving = fields.Float(string="Total Saving", compute="compute_total_saving")

    def _compute_product_our_price_deduct(self):
        for product in self:
            if product.product_template_attribute_value_ids:
                product.our_price_deduct = sum(product.product_template_attribute_value_ids.mapped('our_price_deduct'))
            else:
                if product.product_tmpl_id and product.product_tmpl_id.total_saving:
                    product.our_price_deduct = product.product_tmpl_id.total_saving
                else:
                    product.our_price_deduct = 0.00

    @api.depends('list_price', 'our_price_deduct')
    @api.depends_context('uom')
    def _compute_product_our_price(self):
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse(self._context['uom'])
        for product in self:
            if to_uom:
                list_price = product.uom_id._compute_price(product.list_price, to_uom)
            else:
                list_price = product.list_price
            total_price = list_price + product.price_extra
            if total_price > product.our_price_deduct:
                product.our_price = total_price - product.our_price_deduct
            else:
                product.our_price = 0.00

    def compute_total_saving(self):
        for record in self:
            if record.lst_price:
                record.total_saving = 0.00
                if record.our_price and record.lst_price > record.our_price:
                    record.total_saving = record.lst_price - record.our_price
            else:
                record.total_saving = 0.00


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    our_price = fields.Float(string="Our Price")
    total_saving = fields.Float(string="Total Saving", compute="compute_total_saving")

    @api.depends('list_price', 'our_price')
    def compute_total_saving(self):
        for record in self:
            if record.list_price:
                record.total_saving = 0.00
                if record.our_price and record.list_price > record.our_price:
                    record.total_saving = record.list_price - record.our_price
            else:
                record.total_saving = 0.00

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        """Override for website, where we want to:
            - take the website pricelist if no pricelist is set
            - apply the b2b/b2c setting to the result

        This will work when adding website_id to the context, which is done
        automatically when called from routes with website=True.
        """
        self.ensure_one()
        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if self.env.context.get('website_id'):
            partner = self.env.user.partner_id
            company_id = current_website.company_id
            product = self.env['product.product'].browse(combination_info['product_id']) or self

            tax_display = self.env.user.has_group('account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
            taxes = partner.property_account_position_id.map_tax(product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id))

            # The list_price is always the price of one.
            quantity_1 = 1
            price = taxes.compute_all(combination_info['price'], pricelist.currency_id, quantity_1, product, partner)[tax_display]

            #### Our Price & Total Savings
            our_price = taxes.compute_all(product.our_price, pricelist.currency_id, quantity_1, product, partner)[tax_display]
            total_saving = product.total_saving

            product_template = self.env['product.template'].browse(combination_info['product_template_id'])
            if product_template:
                if pricelist and pricelist.currency_id != product_template.currency_id:
                    our_price = product_template.currency_id._convert(our_price, pricelist.currency_id, product_template._get_current_company(pricelist=pricelist), fields.Date.today())
                    total_saving = product_template.currency_id._convert(total_saving, pricelist.currency_id, product_template._get_current_company(pricelist=pricelist), fields.Date.today())

            if pricelist.discount_policy == 'without_discount':
                list_price = taxes.compute_all(combination_info['list_price'], pricelist.currency_id, quantity_1, product, partner)[tax_display]
            else:
                list_price = price

            has_discounted_price = pricelist.currency_id.compare_amounts(list_price, price) == 1

            combination_info.update(
                price=price,
                list_price=list_price,
                has_discounted_price=has_discounted_price,
                our_price = our_price,
                total_saving = total_saving,
            )
        return combination_info

