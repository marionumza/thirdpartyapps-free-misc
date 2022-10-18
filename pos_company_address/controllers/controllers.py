# -*- coding: utf-8 -*-
# from odoo import http


# class PosCompanyAddress(http.Controller):
#     @http.route('/pos_company_address/pos_company_address', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_company_address/pos_company_address/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_company_address.listing', {
#             'root': '/pos_company_address/pos_company_address',
#             'objects': http.request.env['pos_company_address.pos_company_address'].search([]),
#         })

#     @http.route('/pos_company_address/pos_company_address/objects/<model("pos_company_address.pos_company_address"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_company_address.object', {
#             'object': obj
#         })
