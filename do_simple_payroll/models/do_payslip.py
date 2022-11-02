# -*- coding: utf-8 -*-
#@2022 Abdillah Wahab All Right Reserved
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class DoPayslip(models.Model):
    _name = 'do.payslip'

    
    d_employee_id = fields.Many2one('hr.employee', 'Employee')
    d_start_date = fields.Date('Start Date')
    d_end_date = fields.Date('End Date')
    d_pay_items = fields.One2many('do.payslip.item', 'd_payslip_id', 'Items Payslip')
    d_total_allowance = fields.Float('Total Allowance', compute='_compute_d_total_allowance')
    d_total_deduction = fields.Float('Total Deduction', compute='_compute_d_total_deduction')
    d_take_home_pay = fields.Float('Take Home Pay', compute='_compute_d_take_home_pay')

    @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    def _compute_display_name(self):
        for record in self:
            record.display_name = "%s [%s - %s]"% (record.d_employee_id.name, record.d_start_date, record.d_end_date)

    def _compute_d_total_allowance(self):
        for rec in self:
            rec.d_total_allowance = sum(x.d_total_amount for x in rec.d_pay_items if x.d_category == 'allowance')

    def _compute_d_total_deduction(self):
        for rec in self:
            rec.d_total_deduction = sum(x.d_total_amount for x in rec.d_pay_items if x.d_category == 'deduction')

    def _compute_d_take_home_pay(self):
        for rec in self:
            rec.d_take_home_pay = rec.d_total_allowance - rec.d_total_deduction
            if rec.d_take_home_pay < 0:
                rec.d_take_home_pay = 0

    def _clear_items(self):
        self.d_pay_items.unlink()

    def get_salary(self):
        self._clear_items()
        componets = self.env['do.payslip.component.list'].search([('name', '=', self.d_employee_id.id)])
        items = self._prepare_items(componets)
        self.write({'d_pay_items': items})
        return 

    def _prepare_items(self, components):
        datas = []
        for comp in components:
            quantity = comp.d_component_id.get_quantity(self.d_start_date, self.d_end_date, self.d_employee_id)
            datas.append((0,0, {
                'name': comp.d_component_id.id,
                'd_category': comp.d_component_id.d_category,
                'd_quantity': quantity,
                'd_amount': comp.d_amount,
                'd_total_amount': comp.d_amount * quantity,
            }))
        return datas

class DoPayslipItem(models.Model):
    _name = 'do.payslip.item'

    d_payslip_id = fields.Many2one('do.payslip', 'Payslip')
    name = fields.Many2one('do.payslip.component', 'Component')
    d_category = fields.Selection([('allowance', 'Allowance'), ('deduction', 'Deduction')], 'Category')
    d_quantity = fields.Integer('Quantity')
    d_amount = fields.Float('Amount')
    d_total_amount = fields.Float('Total Amount')

