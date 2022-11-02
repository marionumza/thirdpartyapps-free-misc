# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    commission_type = fields.Selection([
        ('fix', 'Fixed Amount'),
        ('perc', 'Percentage'),
    ])
    commission_amount = fields.Float()
