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


class WasteTypes(models.Model):
    _name = 'waste.types'
    name = fields.Char(string='Type')


class WasteManagement(models.Model):
    _name = 'waste.transfer'
    _rec_name = 'name_id'

    name_id = fields.Many2one('waste.types', string='Type')
    operations_id = fields.Many2one('stock.picking.type')
    responsible_id = fields.Many2one('res.users')
    source_location = fields.Many2one('waste.bins')
    destination_location = fields.Many2one('waste.bins')

