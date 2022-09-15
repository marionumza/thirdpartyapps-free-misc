# -*- coding: utf-8 -*-
# from odoo import http


# class RemitoPreimpreso(http.Controller):
#     @http.route('/remito_preimpreso/remito_preimpreso/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/remito_preimpreso/remito_preimpreso/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('remito_preimpreso.listing', {
#             'root': '/remito_preimpreso/remito_preimpreso',
#             'objects': http.request.env['remito_preimpreso.remito_preimpreso'].search([]),
#         })

#     @http.route('/remito_preimpreso/remito_preimpreso/objects/<model("remito_preimpreso.remito_preimpreso"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('remito_preimpreso.object', {
#             'object': obj
#         })
