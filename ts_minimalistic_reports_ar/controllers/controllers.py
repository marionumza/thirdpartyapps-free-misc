# -*- coding: utf-8 -*-
# from odoo import http


# class ThInvoiceDetail(http.Controller):
#     @http.route('/th_invoice_detail/th_invoice_detail/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/th_invoice_detail/th_invoice_detail/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('th_invoice_detail.listing', {
#             'root': '/th_invoice_detail/th_invoice_detail',
#             'objects': http.request.env['th_invoice_detail.th_invoice_detail'].search([]),
#         })

#     @http.route('/th_invoice_detail/th_invoice_detail/objects/<model("th_invoice_detail.th_invoice_detail"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('th_invoice_detail.object', {
#             'object': obj
#         })
