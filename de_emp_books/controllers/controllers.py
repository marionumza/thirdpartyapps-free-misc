# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmpAccount(http.Controller):
#     @http.route('/de_emp_account/de_emp_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_emp_account/de_emp_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_emp_account.listing', {
#             'root': '/de_emp_account/de_emp_account',
#             'objects': http.request.env['de_emp_account.de_emp_account'].search([]),
#         })

#     @http.route('/de_emp_account/de_emp_account/objects/<model("de_emp_account.de_emp_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_emp_account.object', {
#             'object': obj
#         })
