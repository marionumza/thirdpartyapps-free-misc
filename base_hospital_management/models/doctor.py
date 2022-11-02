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

from odoo import models, fields


class HospitalDoctors(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Selection(string='Designation',
                                 selection=[('employee', 'Employee'), ('doctor', 'Doctor')],
                                 default='employee')
    pharmacy_id = fields.Many2one('hospital.pharmacy', string="Pharmacy", required=True)
    consultancy_charge = fields.Monetary(string="Consultancy Charge")
    consultancy_type = fields.Selection([('resident', 'Residential'),
                                         ('special', 'Specialist')],
                                        string="Consultancy Type")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    degrees = fields.Many2many('hospital.degree', string="Degrees")
    institute = fields.Many2many('hospital.institution',
                                 string="Institution Name")
    specialization = fields.Many2many('hospital.specialization',
                                      string="Specialization", help="Doctors specialization for an area")
    prescription_ids = fields.One2many('hospital.prescription', 'pharmacy_id', 'Prescription')
    pharmacy_ids = fields.One2many('hospital.pharmacy', 'doctor_id', 'Pharmacy')
