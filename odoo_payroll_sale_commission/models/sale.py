# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    employee_commission_amount = fields.Monetary(compute='get_employee_commission_amount', store=True)

    @api.depends('amount_total')
    def get_employee_commission_amount(self):
        for order in self:
            employee_commission_amount = 0
            if order.user_id:
                related_employee = self.env['hr.employee'].search([('user_id', '=', order.user_id.id)], limit=1)
                if related_employee and related_employee.commission_type and related_employee.commission_amount:
                    if related_employee.commission_type == 'fix':
                        employee_commission_amount = related_employee.commission_amount
                    else:
                        employee_commission_amount = order.amount_total * related_employee.commission_amount / 100

            order.employee_commission_amount = employee_commission_amount
