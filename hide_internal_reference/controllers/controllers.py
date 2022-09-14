# -*- coding: utf-8 -*-
# from odoo import http


# class HideInternalReference(http.Controller):
#     @http.route('/hide_internal_reference/hide_internal_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_internal_reference/hide_internal_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_internal_reference.listing', {
#             'root': '/hide_internal_reference/hide_internal_reference',
#             'objects': http.request.env['hide_internal_reference.hide_internal_reference'].search([]),
#         })

#     @http.route('/hide_internal_reference/hide_internal_reference/objects/<model("hide_internal_reference.hide_internal_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_internal_reference.object', {
#             'object': obj
#         })
