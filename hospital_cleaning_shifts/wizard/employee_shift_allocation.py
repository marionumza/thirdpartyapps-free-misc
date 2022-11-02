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
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class EmployeeShift(models.TransientModel):
    _name = 'employee.shift.wizard'

    employee_id = fields.Many2one('hr.employee')
    date_from = fields.Date()
    date_to = fields.Date()
    shift_id = fields.Many2one('employee.shift')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')

    def allocate_shift(self):
        vals = []
        employee_shift_duplication = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        for rec in employee_shift_duplication.employee_shift:
            if rec.date_from == self.date_from and rec.date_to == self.date_to:
                raise ValidationError(_(
                    "The Shift Is Already Allocated"
                ))
            else:
                for rec in self:
                    teams = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    vals.append((0, 0, {'date_from': self.date_from,
                                        'date_to': self.date_to,
                                        'shift_id': self.shift_id.name,
                                        'employee_id': self.employee_id,
                                        'name': self.shift_id.name,
                                        'department_id': self.department_id.id,
                                        }))
                    vals.append(vals)
                teams.employee_shift = vals

    def shift_allocations(self):
        if self.employee_id and self.date_from and self.date_to and self.shift_id:
            return {
                'name': 'Shifts',
                'domain': [('employee_id.id', '=', self.employee_id.id), ('date_from', '>=', self.date_from),
                           ('date_to', '<=', self.date_to)],
                'type': 'ir.actions.act_window',
                'res_model': 'employee.shift',
                'view_mode': 'tree',
                'context': {'create': False},
            }

        domain = []
        shift_id = self.shift_id
        if shift_id:
            domain += [('shift_id', '=', shift_id.id)]
        date_from = self.date_from
        if date_from:
            domain += [('date_from', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('date_to', '<=', date_to)]
        employee_shifts = self.env['employee.shift'].search_read(domain)

        data = {
            'employee_id': self.ids,
            'date_from': self.date_from,
            'to_date': self.date_to,
            'shift_id': self.shift_id,
            'employee_shifts': employee_shifts,
            'form_data': self.read()[0],

        }
        return self.env.ref(
            'hospital_cleaning_shifts.action_shift_report').report_action(self, data=data)
