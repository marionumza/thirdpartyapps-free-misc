# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt. Ltd. <www.botspotinfoware.com>
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
from datetime import date, time


class RepairLine(models.Model):
    _inherit = "repair.line"

    is_purchase_part_show = fields.Boolean(string="Is Purchase Part Show")

    def action_Purchase_part(self):
        self.ensure_one()
        purchase_order = self.env['purchase.order'].search([(
            'repair_order_id', '=', self.repair_id.id)])
        context = {'default_repair_order_id': self.repair_id.id,
                   'default_order_line': [(0, 0, {"product_id": self.id,
                                                  "name": self.name,
                                                  "product_qty": self.product_uom_qty,
                                                  "price_unit": self.price_unit,
                                                  "product_uom": self.product_uom.id,
                                                  "date_planned": date.today()})]}
        return {
          'res_model': 'purchase.order',
          'type': 'ir.actions.act_window',
          'context': context,
          'view_mode': 'form',
          'view_type': 'form',
          'target': 'new',
        }

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_product_id(self):
        if self.product_id:
            if self.product_uom_qty > self.product_id.qty_available:
                self.is_purchase_part_show = True
            else:
                self.is_purchase_part_show = False


class Repair(models.Model):
    _inherit = "repair.order"

    purchase_count = fields.Integer(
        string="Purchases", compute="compute_count")

    def compute_count(self):
        for record in self:
            record.purchase_count = self.env['purchase.order'].search_count([(
                'repair_order_id', '=', record.id)])

    def get_purchase_part(self):
        self.ensure_one()
        return{
            'name': 'purchases',
            'res_model': 'purchase.order',
            'domain': [('repair_order_id', '=', self.id)],
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'context': "{'create': False}"
        }
