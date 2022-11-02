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
from datetime import date, timedelta


class Lab(models.Model):
    _name = 'hospital.labs'
    _description = 'Lab'
    _rec_name = 'name'

    name = fields.Char('Lab', required="True")
    institution_id = fields.Many2one('hospital.hospital', string="Institution", required=True)
    building_id = fields.Many2one('hospital.buildings', 'Block', required=True)
    ward_no = fields.Many2one('hospital.wards', 'Ward', required=True)
    notes = fields.Text()
    image_130 = fields.Image(max_width=128, max_height=128)
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    labs_phone = fields.Char(' Phone')
    labs_mobile = fields.Char(' Mobile')
    labs_email = fields.Char(' Email')
    labs_address = fields.Char('Work Address')
    labs_street = fields.Char('Street')
    labs_street2 = fields.Char('Street2')
    labs_zip = fields.Char('Zip')
    labs_city = fields.Char('City')
    labs_state_id = fields.Many2one("res.country.state", string='State')
    labs_country_id = fields.Many2one('res.country', string='Country')
    labs_note = fields.Text('Note')
    lab_seq = fields.Char(string='Lab Sequence', required=True,
                          copy=False,
                          readonly=True,
                          index=True,
                          default=lambda self: 'New')
    technician_id = fields.Many2one('hr.employee', string="Lab in charge",
                                    domain=[('job_title', '=', 'Lab Technician')])

    @api.onchange('institution_id')
    def _ward_bed(self):
        """basis of institute the wards bed is computed"""

        return {'domain': {
            'building_id': [
                ('institution_id', '=', self.institution_id.id),
            ]}}

    @api.onchange('building_id')
    def _ward(self):
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    @api.model
    def create(self, vals):
        if vals.get('lab_seq', 'New') == 'New':
            vals['lab_seq'] = self.env['ir.sequence'].next_by_code(
                'lab.sequence') or 'New'
        result = super(Lab, self).create(vals)
        return result
