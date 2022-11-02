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


class HospitalSurgery(models.Model):
    _name = 'hospital.operation'
    _rec_name = 'op_room_name'

    op_room_name = fields.Char('Name', required="True")
    state = fields.Selection(
        [('free', 'Free'), ('reserved', 'Reserved'), ('occupied', 'Occupied'), ('unavailable', 'Not Available')],
        default='free')
    building_id = fields.Many2one('hospital.buildings', string="Block")
    surgery_id = fields.Many2one('hospital.surgery')
    text = fields.Html('Notes')
