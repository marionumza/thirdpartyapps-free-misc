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
from odoo.fields import Date


class CleaningTeams(models.Model):
    _name = 'cleaning.teams'
    _rec_name = 'team_name'

    team_name = fields.Char(string='Name')
    team_lead = fields.Many2one('hr.employee', string='Team Leader')
    category = fields.Many2one('team.category', string='Category')
    responsible = fields.Many2one('res.users', string='Responsible User')
    members_ids = fields.One2many('team.category', 'inverse_id')
    department_id = fields.Many2one('hr.department', string='Department')
    institution_id = fields.Many2one('hospital.hospital', string="Institution")
    building_name = fields.Many2one('hospital.buildings', string="Block")
    shift_name_id = fields.Many2one('employee.shift', string="Shift")
    dirty = fields.Boolean()
    clean = fields.Boolean()
    date_from = fields.Date()
    date_to = fields.Date()
    inverse_field_id = fields.Many2one('cleaning.inspection')
    date = fields.Date(default=Date.today())

    def cleaning_inspect(self):
        """each teams cleaning work is inspected"""
        rslt = self.env['cleaning.inspection'].create({
            'cleaning_team': self.id,
            'department_id': self.department_id.name,
            'building_name': self.building_name.id,
            'cleaning_team_inspect_id': [
                (0, 0, {
                    'shift_name_id': t.id,
                    'date_from': t.date_from,
                    'date_to': t.date_to,

                }) for t in self.shift_name_id]
        })
        return {
            'res_model': 'cleaning.inspection',
            'type': 'ir.actions.act_window',
            'res_id': rslt.id,
            'view_mode': 'form',
            'name': 'Inspection',
            'target': 'current',
            'context': "{'create': False ,}"
        }


class CleaningTeamsCategory(models.Model):
    _name = 'team.category'
    inverse_id = fields.Many2one('cleaning.teams')
    partner_name_id = fields.Many2one('hr.employee', string='Members')
    responsible = fields.Many2one('res.users', string='Responsible User')
