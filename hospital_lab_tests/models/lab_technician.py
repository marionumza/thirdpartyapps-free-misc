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


class Doctor(models.Model):
    _name = 'lab.technician'
    _description = 'Lab Technician'
    _rec_name = 'technician_name'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    technician_name = fields.Char(string="Name")
    employee_id = fields.Many2one('hr.employee', 'Employee ID')
    degrees = fields.Many2many('hospital.degree', string="Degrees")
    institute = fields.Many2many('hospital.institution',
                                 string="Institution Name")
    specialization = fields.Many2many('hospital.specialization',
                                      string="Specialization")
    licence = fields.Char(string="Licence ID")
    visa_no = fields.Char(string="Visa No.")
    permit_no = fields.Char(string="Work Permit No.")
    expire_date = fields.Date(string="Visa Expire Date")
    place_of_birth = fields.Char('Place of Birth')
    birthday = fields.Date(string="Date of Birth")
    country_of_birth_id = fields.Many2one('res.country', string='Country of '
                                                                'Birth')
    work_phone = fields.Char(' Phone')
    work_mobile = fields.Char(' Mobile')
    work_email = fields.Char(' Email')
    work_address = fields.Char('Work Address')
    work_street = fields.Char('Street')
    work_street2 = fields.Char('Street2')
    work_zip = fields.Char('Zip')
    work_city = fields.Char('City')
    work_state_id = fields.Many2one("res.country.state", string='State')
    work_country_id = fields.Many2one('res.country', string='Country')
    work_location = fields.Char('Work Location')
    pvt_phone = fields.Char('Phone')
    pvt_mobile = fields.Char('Mobile')
    pvt_email = fields.Char('Email')
    pvt_address = fields.Char(' Address')
    spouse_complete_name = fields.Char("Spouse's Name")
    spouse_birthdate = fields.Date(string="Date of Birth")
    children = fields.Integer(string='Number of Children')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Nationality(Country)')
    identification_no = fields.Char('Identification No')
    passport_no = fields.Char('Passport No')
    account_no = fields.Char('Bank Account No')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string="Gender")
    availability = fields.Char('Availability')
    status = fields.Selection([('unmarried', 'Unmarried'),
                               ('married', 'Married'),
                               ],
                              string="Marital Status")
    image_131 = fields.Image(max_width=128, max_height=128)


