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
from odoo import api,fields,models,_

#Class was Extended to add the Functionality of Actual Sales Amount and Actual Sales Percentage.
class CrmLead(models.Model):

    _inherit = "crm.lead"
  
     
    actual_sales = fields.Float(string="Actual Sales", compute="compute_actual_sales", track_visibility='always', help = "Field Gives The value Of Actual sales For Current Opportunity From The Sale Order ")
    actual_sales_pr= fields.Float(string="Actual Sales Percentage", compute="compute_actual_sales_pr", track_visibility='always',  help = "Field Gives The value Of Actual Sales Percentage For Current Opportunity From The Sale Order ")

    #Method compute The Actual Sale Order from Whole Sale Order List
    @api.depends('order_ids')
    def compute_actual_sales(self):
        for record in self:
            total_actual_sales_amount_in_opp = 0
            for order in record.order_ids:
                if order.state in ['sale', 'done']:
                    total_actual_sales_amount_in_opp = order.amount_total + total_actual_sales_amount_in_opp
        record.actual_sales = total_actual_sales_amount_in_opp

    #Method compute The Actual Sale Order Percentage from Whole Sale Order List
    @api.depends('order_ids')
    def compute_actual_sales_pr(self):
        for record in self:
            if record.actual_sales_pr:
                continue  
            if record.actual_sales * record.probability !=0:
                record.actual_sales_pr = (record.actual_sales * 100)/record.planned_revenue
