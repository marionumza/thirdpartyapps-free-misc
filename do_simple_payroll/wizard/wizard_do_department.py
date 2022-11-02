# -*- coding: utf-8 -*-
#@2022 Abdillah Wahab All Right Reserved
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class DoChooseDepartment(models.TransientModel):
    _name = 'wizdo.choose.department'

    d_department_id = fields.Many2one('hr.department', 'Department')
    d_component_id = fields.Many2one('do.payslip.component', 'Component')

    def choose(self):
        return self.d_component_id.add_all_employee(self.d_department_id)

