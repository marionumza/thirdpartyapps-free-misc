# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectField(http.Controller):
#     @http.route('/project_field/project_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_field/project_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_field.listing', {
#             'root': '/project_field/project_field',
#             'objects': http.request.env['project_field.project_field'].search([]),
#         })

#     @http.route('/project_field/project_field/objects/<model("project_field.project_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_field.object', {
#             'object': obj
#         })
