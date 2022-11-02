""""Hospital Management"""
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


class RoomAssign(models.TransientModel):
    """Wizard for selecting the patient details in hospital"""
    _name = 'room.view'
    _description = 'room_assigning'

    patient_id = fields.Many2one('res.partner', 'Patient')
    responsible_person = fields.Many2one('hr.employee', help="The person who take care of the patient")
    visting_time = fields.Float()
    room_no = fields.Many2one('patient.room')

    def patient_room_assigning(self):
        """updating the room for patients"""
        print(self.room_no,'rkjmkjm')
        val = self.env['hospital.inpatient'].search([('patient_id','=',self.patient_id.id)])
        val.write({
            'room_no' : self.room_no
        })
