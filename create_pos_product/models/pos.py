# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models


class pos_inherited(models.Model):
    _inherit = 'pos.config'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
