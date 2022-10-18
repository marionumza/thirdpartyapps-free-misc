# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class pos_company_address(models.Model):
#     _name = 'pos_company_address.pos_company_address'
#     _description = 'pos_company_address.pos_company_address'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
