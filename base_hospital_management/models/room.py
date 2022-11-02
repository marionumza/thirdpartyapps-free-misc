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
from odoo import models, fields,api


class Room(models.Model):
    _name = 'patient.room'
    _description = 'Room'
    _rec_name = 'room_no'

    room_no = fields.Char(string="Room No.")
    bed_id = fields.Many2one('hospital.beds', string="Bed No.")
    facilities_ids = fields.Many2many('hospital.facilities',
                                      string="Facilities")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    building_id = fields.Many2one('hospital.buildings', string="Block Name",
                                  required="True")
    ward_id = fields.Many2one('hospital.wards', string="Ward No.",)
    rent = fields.Monetary(string='Rent')
    _sql_constraints = [('unique_room', 'unique (ward_no)',
                         'Room number should be unique!')]
    state = fields.Selection([('avail', 'Available'), ('reserve', 'Reserve'), ('not', 'Unavailable'), ],
                             string='State', readonly=True,
                             default="avail")

    @api.onchange('building_id')
    def _onchange_ward(self):
        """ward creation in building"""
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    @api.onchange('ward_id')
    def _onchange_ward_beds(self):
        """available beds calculation"""
        return {'domain': {
            'bed_id': [
                ('ward_id', '=', self.ward_id.id),
                ('state', '=', 'avail')
            ]}}

    def action_room_assign(self):
        """assigning rooms"""
        self.state = 'not'

        return{
            'name': "Assign Rooms",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'room.view',
            'view_id': self.env.ref("base_hospital_management.room_wizard").id,
            'target': 'new',
            'context': {'default_room_no': self.id},
        }






