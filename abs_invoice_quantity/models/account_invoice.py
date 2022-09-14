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

class AccountMove(models.Model):
    _inherit = "account.move"

    total_product = fields.Integer(string='Total Product:',compute='_total_product',help="total Products")
    total_quantity = fields.Integer(string='Total Quantity:',compute='_total_quantity',help="total Quantity")

    def _total_product(self):
        for record in self:
            product_list=[]
            for line in record.invoice_line_ids:
                product_list.append(line.product_id)
            record.total_product = len(set(product_list))

    def _total_quantity(self):
        for record in self:
            total_qty = 0
            for line in record.invoice_line_ids:
                total_qty = total_qty + line.quantity
            record.total_quantity = total_qty
