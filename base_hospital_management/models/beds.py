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
from odoo.fields import Date


class Beds(models.Model):
    _name = 'hospital.beds'
    _description = 'Beds'
    _rec_name = 'bed_no'

    bed_no = fields.Char(string="Bed No.", required="True")
    _sql_constraints = [('unique_room', 'unique (bed_no)',
                         'Bed number should be unique!')]
    bed_type = fields.Selection([('gatch', 'Gatch Bed'),
                                 ('electric', 'Electric'),
                                 ('stretcher', 'Stretcher'),
                                 ('low', 'Low Bed'),
                                 ('air', 'Low Air Loss'),
                                 ('circo', 'Circo Electric'),
                                 ('clinitron', 'Clinitron'),
                                 ], string="Bed Type",
                                )
    note = fields.Text(string="Notes")
    date_bed_assign = fields.Date(default=Date.today(), string='Date')
    ward_id = fields.Many2one('hospital.wards', string="Ward No.",)
    institution_id = fields.Many2one('hospital.hospital', string="Institution")
    building_id = fields.Many2one('hospital.buildings', string="Block")

    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id,
                                  required=True)
    repair_charge = fields.Monetary(string='Repair Charge',help="The repairing charge whether any damage is happened")
    bed_rent = fields.Monetary(string='Rent', help="The charge for the bed")
    repair_date = fields.Date(string='Repair Date', help="The next repairing sate")
    state = fields.Selection([('avail', 'Available'), ('not', 'Unavailable')], string='State', readonly=True,
                             default="avail")

    @api.onchange('institution_id')
    def _onchange_ward_bed(self):
        """building"""
        return {'domain': {
            'building_id': [
                ('institution_id', '=', self.institution_id.id),
            ]}}

    @api.onchange('building_id')
    def _onchange_ward(self):
        """ward"""
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    def action_assign(self):
        """state"""
        self.state = "not"






