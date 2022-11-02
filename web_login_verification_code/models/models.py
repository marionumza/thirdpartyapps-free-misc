# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class d:\work\hey_odoo_15\app\web_login_verification_code(models.Model):
#     _name = 'd:\work\hey_odoo_15\app\web_login_verification_code.d:\work\hey_odoo_15\app\web_login_verification_code'
#     _description = 'd:\work\hey_odoo_15\app\web_login_verification_code.d:\work\hey_odoo_15\app\web_login_verification_code'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
