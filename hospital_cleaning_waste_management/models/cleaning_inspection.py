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
from odoo.exceptions import UserError


class CleaningInspection(models.Model):
    """After cleaning, it is inspected by inspection officer"""
    _name = 'cleaning.inspection'
    _rec_name = 'cleaning_team'

    date = fields.Date()
    cleaning_type = fields.Many2one('cleaning.types')
    inspector = fields.Many2one('res.users')
    cleaning_team = fields.Many2one('cleaning.teams')
    department_id = fields.Char()
    notes = fields.Text('Notes')
    building_name = fields.Char(string="Block", required="True")
    cleaning_team_inspect_id = fields.One2many('cleaning.teams',
                                               'inverse_field_id')
    state = fields.Selection([('draft', 'Draft'), ('clean', 'Clean'),
                              ('dirty', 'Dirty')], default='draft')

    def cleaning_inspect_done(self):
        """cleaning is inspcted after that the inspector specifies that is
        clean or dirty """
        for rec in self.cleaning_team_inspect_id:
            if rec.clean == True:
                self.state = 'clean'
            elif rec.dirty == True:
                self.state = 'dirty'
            else:
                raise UserError('Make sure that you marked your '
                                'Result.........!')


class CleaningTypes(models.Model):
    _name = 'cleaning.types'
    name = fields.Char()
