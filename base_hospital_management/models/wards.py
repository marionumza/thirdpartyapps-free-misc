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


class Wards(models.Model):
    _name = 'hospital.wards'
    _description = 'Wards'
    _rec_name = 'ward_no'

    ward_no = fields.Char(string="Ward Name", required="True")
    building_id = fields.Many2one('hospital.buildings', string="Block Name")


    floor_no = fields.Integer(string="Floor No.")
    facilities = fields.Many2many('ward.facilities', string="Facilities")
    note = fields.Text(string="Note")
    bed_count = fields.Integer(string="Count", compute="_compute_count")

    _sql_constraints = [('unique_ward', 'unique (ward_no)',
                         'Ward number should be unique!')]


    @api.onchange('building_id')
    def _onchange_ward_beds(self):
        return {'domain': {
            'bed_id': [
                ('ward_id', '=', self.id),
            ]}}

    def open_bed(self):
        """bed creation form"""
        return {
            'name': 'Bed',
            'domain': [('ward_id', '=', self.ward_no)],
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.beds',
            'view_mode': 'tree',
            'context': {'create': False},
        }

    def _compute_count(self):
        """bed count"""
        count = self.env['hospital.beds'].search_count([(
            'ward_id', '=', self.ward_no)])

        self.bed_count = count
