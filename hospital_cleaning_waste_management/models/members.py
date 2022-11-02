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


class Members(models.Model):
    """members in the cleaning team"""
    _inherit = 'hr.employee'
    name = fields.Char(string="Name")

    team_name = fields.Char(string='Name')
    team_lead = fields.Char(string='Team Leader')
    category = fields.Many2one('team.category', string='Category')
    responsible = fields.Many2one('res.users', string='Responsible User')
    members_ids = fields.One2many('team.category', 'partner_name_id')
    check_in = fields.Float(string='Check In')
    Check_out = fields.Float(string='Check Out')
    status = fields.Selection([('married', 'Married'),
                               ('unmarried', 'Unmarried')],
                              string="Marital Status", required=True)
    gender = fields.Selection([('female', 'Female'),
                               ('male', 'Male'),
                               ('others', 'Other')],
                              string="Gender", required=True)
    profession = fields.Char(string="Profession")
