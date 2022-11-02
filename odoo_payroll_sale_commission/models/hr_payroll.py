# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayroll(models.Model):
    _inherit = 'hr.payslip'

    employee_commission_amount = fields.Monetary(compute="get_employee_commission_amount", store=True)

    @api.depends('employee_id', 'date_from', 'date_to')
    def get_employee_commission_amount(self):
        self = self.sudo()
        for payslip in self:
            employee_commission_amount = 0
            related_user = payslip.employee_id.user_id
            if related_user:
                sale_orders = self.env['sale.order'].search([
                    ('user_id', '=', related_user.id),
                    ('date_order', '>=', payslip.date_from),
                    ('date_order', '<=', payslip.date_to),
                    ('state', 'in', ['sale', 'done']),
                ])
                employee_commission_amount = sum(sale_orders.mapped('employee_commission_amount'))
            payslip.employee_commission_amount = employee_commission_amount
