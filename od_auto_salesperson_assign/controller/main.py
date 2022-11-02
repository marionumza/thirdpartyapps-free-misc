# -*- coding: utf-8 -*-
from datetime import date
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFormInherit(WebsiteSale):
    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True, sitemap=False)
    def confirm_order(self, **post):
        order = request.website.sale_get_order()
        condition = True
        if not order.user_id:
            if order.partner_id and order.company_id.existing_order_bool:
                existing_sale_order = request.env['sale.order'].sudo().search(
                    [('partner_id', '=', order.partner_id.id), ('id', '!=', order.id)], limit=1)
                if existing_sale_order:
                    condition = False
                    order.user_id = existing_sale_order.user_id
            if condition:
                if order.company_id.user_id_selection == 'by_default':
                    order.user_id = order.company_id.default_user_id
                if order.company_id.user_id_selection == 'by_day':
                    for day in order.company_id.day_ids:
                        if int(day.day_selection) == date.today().weekday():
                            order.user_id = day.user_id
                if order.company_id.user_id_selection == 'by_state':
                    for state_line in order.company_id.line_state_ids:
                        if order.partner_id.state_id in state_line.res_state_ids:
                            order.user_id = state_line.user_id
                if order.company_id.user_id_selection == 'by_website':
                    for state in order.company_id.website_ids:
                        if state.website_id == order.website_id:
                            order.user_id = state.user_id
        redirection = self.checkout_redirection(order) or self.checkout_check_address(order)
        if redirection:
            return redirection
        order.onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)
        extra_step = request.website.viewref('website_sale.extra_info_option')
        if extra_step.active:
            return request.redirect("/shop/extra_info")
        return request.redirect("/shop/payment")
