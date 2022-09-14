# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _

class StockLocation(models.Model):
    _inherit = "stock.location"

    def _default_stage_id(self):
        stages = self.env['location.condition'].search([])
        stage_list = []
        stages_final = False
        stage_return = False
        for stage in stages:
            stage_list.append(stage.sequence)
        if stage_list:
            stage_return = min(stage_list)
        if stage_return:
            stages_final = self.env['location.condition'].search([('sequence','=',stage_return)])[0]
        if stages_final:
            return stages_final.id
        else:
            return False

    stage_id = fields.Many2one('location.condition', string='Conditions', default=lambda self: self._default_stage_id(), track_visibility='onchange', copy=False)


