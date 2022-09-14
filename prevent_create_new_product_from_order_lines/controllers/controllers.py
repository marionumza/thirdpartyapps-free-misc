# -*- coding: utf-8 -*-
# from odoo import http


# class PreventCreateNewProductOnOrderLines(http.Controller):
#     @http.route('/prevent_create_new_product_from_order_lines/prevent_create_new_product_from_order_lines/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prevent_create_new_product_from_order_lines/prevent_create_new_product_from_order_lines/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('prevent_create_new_product_from_order_lines.listing', {
#             'root': '/prevent_create_new_product_from_order_lines/prevent_create_new_product_from_order_lines',
#             'objects': http.request.env['prevent_create_new_product_from_order_lines.prevent_create_new_product_from_order_lines'].search([]),
#         })

#     @http.route('/prevent_create_new_product_from_order_lines/prevent_create_new_product_from_order_lines/objects/<model("prevent_create_new_product_from_order_lines.prevent_create_new_product_from_order_lines"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prevent_create_new_product_from_order_lines.object', {
#             'object': obj
#         })
