# -*- coding: utf-8 -*-
#@2022 Abdillah Wahab All Right Reserved
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    d_validate = fields.Selection([('unchecked', 'Unchecked'), ('valid', 'Approved')], 'Validation', default='unchecked')

    def set_validate(self):
        return self.write({'d_validate': 'valid'})
