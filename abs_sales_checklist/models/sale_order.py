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
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_history_ids = fields.One2many('sale.task.history','order_id',string='Tasks')

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        products = []
        if vals.get('order_line'):
            for product in vals.get('order_line'):
                if product[2] and product[2].get('product_id'):
                    products.append(product[2]['product_id'])
        task_history_obj = self.env['sale.task.history']
        tasks = []
        unique_task = []
        product_ids = self.env['product.product'].search([('id', 'in', products)])
        for curr_product in product_ids:
            for task in curr_product.task_ids:
                tasks.append(task.id)
        if tasks:
            unique_task = set(tasks)
        for curr_task in unique_task:
            vals = {'order_id':res.id , 'sale_task_id':curr_task}
            task_history_obj.sudo().create(vals)
        return res


    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        products = []
        if vals.get('order_line'):
            for product in vals.get('order_line'):
                if product[2] and product[2].get('product_id'):
                    products.append(product[2]['product_id'])
        task_history_obj = self.env['sale.task.history']
        tasks = []
        unique_task = []
        old_tasks = [] 
        sale_task_history = self.env['sale.task.history'].search([('order_id', '=', self.id)])
        for task_history in sale_task_history:
            old_tasks.append(task_history.sale_task_id)
        product_ids = self.env['product.product'].search([('id', 'in', products)])
        for curr_product in product_ids:
            for task in curr_product.task_ids:
                if task not in old_tasks:
                    tasks.append(task.id)
        if tasks:
            unique_task = set(tasks)
        for curr_task in unique_task:
            vals = {'order_id':self.id , 'sale_task_id':curr_task}
            task_history_obj.sudo().create(vals)
        return res


    def action_confirm(self):
        tasks = []
        for task in self:
            for record in task.task_history_ids:
                if record:
                    if not record.done:
                        raise ValidationError(_('Please mark all tasks done to confirm this order!'))            
        res = super(SaleOrder, self).action_confirm() 
        return res
