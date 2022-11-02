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


class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hospital'
    _rec_name = 'hosp_name'
    hosp_name = fields.Char(string="Name", help="Name of the hospital")
    hosp_type = fields.Selection([('hospital', 'Hospital'),
                                  ('multi', 'Multi-Hospital'),
                                  ('nursing', 'Nursing-Home'),
                                  ('clinic', 'Clinic'),
                                  ('community', 'Community-Health Center'),
                                  ('military', 'Military Medical Center'),
                                  ('other', 'Other')],
                                 string="Institution Type")
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    hosp_phone = fields.Char(' Phone')
    hosp_mobile = fields.Char(' Mobile')
    hosp_email = fields.Char(' Email')
    hosp_address = fields.Char('Work Address')
    hosp_street = fields.Char('Street')
    hosp_street2 = fields.Char('Street2')
    hosp_zip = fields.Char('Zip')
    hosp_city = fields.Char('City')
    hosp_state_id = fields.Many2one("res.country.state", string='State')
    hosp_country_id = fields.Many2one('res.country', string='Country')
    note = fields.Text('Note')
    image_129 = fields.Image(max_width=128, max_height=128)

