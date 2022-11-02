# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        sales = super(SaleOrder, self).create(vals)
        if vals.get('user_id'):
            condition = True
            for order in sales:
                if order.partner_id and order.company_id.existing_order_bool:
                    existing_sale_order = self.search(
                        [('partner_id', '=', order.partner_id.id), ('id', '!=', order.id)], limit=1)
                    if existing_sale_order:
                        condition = False
                        order.user_id = existing_sale_order.user_id
                if condition:
                    if order.company_id.user_id_selection == 'by_default':
                        order.user_id = order.company_id.default_user_id
                    if order.company_id.user_id_selection == 'by_day':
                        for day in order.company_id.day_ids:
                            if int(day.day_selection) == fields.date.today().weekday():
                                order.user_id = day.user_id
                    if order.company_id.user_id_selection == 'by_state':
                        for state_line in order.company_id.line_state_ids:
                            if order.partner_id.state_id in state_line.res_state_ids:
                                order.user_id = state_line.user_id
                    if order.company_id.user_id_selection == 'by_website':
                        for state in order.company_id.website_ids:
                            if state.website_id == order.website_id:
                                order.user_id = state.user_id
        return sales
