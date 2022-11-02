# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import fields, models
from odoo.fields import Date


class EmployeeShifts(models.Model):
    """employees shift management"""
    _name = 'employee.shift'
    _description = 'employee_shifts'

    name = fields.Char(string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    institution_id = fields.Many2one('hospital.hospital', string="Institution")
    inverse_id = fields.Many2one('hr.employee')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    shift_id = fields.Char(help="employees shift id")
    employee_id = fields.Many2many('hr.employee')
    date = fields.Date(default=Date.today())

    def confirm_shift(self):
        """Assigning shift to Employees"""
        vals = []
        for rec in self:
            teams = self.env['hr.employee'].search(
                [('department_id', '=', rec.department_id.id)])
            vals.append((0, 0, {'date_from': self.date_from,
                                'date_to': self.date_to,
                                'shift_id': self.name,

                                }))
            vals.append(vals)
        teams.employee_shift = vals


class ShiftTypes(models.Model):
    """The Type of Shifts morning night etc"""
    _name = 'shift.types'
    name = fields.Char()
    shift_type = fields.Many2one('employee.shift')


class Employee(models.Model):
    """Adding a one2many fields to employee to update the shift"""
    _inherit = 'hr.employee'

    employee_shift = fields.One2many('employee.shift', 'inverse_id')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    shift_id = fields.Char()
