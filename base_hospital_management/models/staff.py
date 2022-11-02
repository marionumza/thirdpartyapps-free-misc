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
from odoo import models, fields, api


class Staff(models.Model):
    _name = 'hospital.staffs'
    _description = 'Staff'
    department_id = fields.Many2one('hr.department', string="Department",
                                    )
    staff_id = fields.Many2many('hr.employee', string="Staff",
                                readonly='1')
    _rec_name = 'department_id'

    @api.onchange('department_id')
    def _onchange_department(self):
        """staffs taking basis of department"""
        for rec in self:
            rec.staff_id = rec.env['hr.employee'].search([('department_id', '=',
                                                       rec.department_id.name)])
