# -*- coding: utf-8 -*-
from odoo import http

# class DeactivateExpiredEmployeeUser(http.Controller):
#     @http.route('/deactivate_expired_employee_user/deactivate_expired_employee_user/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/deactivate_expired_employee_user/deactivate_expired_employee_user/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('deactivate_expired_employee_user.listing', {
#             'root': '/deactivate_expired_employee_user/deactivate_expired_employee_user',
#             'objects': http.request.env['deactivate_expired_employee_user.deactivate_expired_employee_user'].search([]),
#         })

#     @http.route('/deactivate_expired_employee_user/deactivate_expired_employee_user/objects/<model("deactivate_expired_employee_user.deactivate_expired_employee_user"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('deactivate_expired_employee_user.object', {
#             'object': obj
#         })