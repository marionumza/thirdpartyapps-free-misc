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
from odoo import models, fields, api, _
from odoo.fields import Date


class TestCommission(models.Model):
    _name = 'test.commission'
    _rec_name = 'employee_id'
    _description = 'Employee Commission'

    employee_id = fields.Many2one('hr.employee')
    employee_commission = fields.Many2one('commission.configuration', 'Commission',
                                          domain="[('employee_id', '=', employee_id),('expiry_date','>',date)]")
    date = fields.Date('Date', default=Date.today())
    test_id = fields.Many2one('hospital.laboratory', string='Test')
    commission_medicine_ids = fields.One2many('commission.configurations.lines', 'medi_commission_id')
    test_commission_lines_ids = fields.One2many('test.commission.lines', 'test_commission_id', 'Test Lines')
    test_commission_id = fields.Many2one('commission.configurations.lines')
    commission = fields.Float("Commission")
    amount_total = fields.Monetary('Total', compute='_onchange_compute_amount_total')
    amount_total_medicine = fields.Monetary('Total Price', compute='compute_medicine_total')

    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)

    @api.onchange('employee_commission')
    def onchange_employee_commission(self):
        """compute the commission lines on a employee for medicine"""
        for rec in self:
            a = self.env['commission.configuration'].search(
                [('employee_id', '=', rec.employee_id.id)])
            rec.commission_medicine_ids = [(5, 0, 0)]
            for line in a.commission_ids:
                vals = {
                    'product_ids': line.product_ids,
                    'count': self.env['hospital.prescription'].search_count(
                        [('medicine_id', '=', line.product_ids.id)]),
                    'commission_percentage': line.commission_percentage,
                    'amount': line.price,
                }
                rec.commission_medicine_ids = [(0, 0, vals)]

    @api.onchange('employee_commission')
    def onchange_employee_commission_test(self):
        """compute the commission lines on a employee for test"""
        for rec in self:
            a = self.env['commission.configuration'].search(
                [('employee_id', '=', rec.employee_id.id)])
            print(a)
            rec.test_commission_lines_ids = [(5, 0, 0)]
            for line in a.commission_test_ids:
                print(line)
                vals = {
                    'test_id': line.id,
                    'commission': line.commission_percentage,
                    'count': self.env['test.test'].search_count([('id', '=', line.product_ids.id)]),
                    'comm_price': line.price,
                }
                rec.test_commission_lines_ids = [(0, 0, vals)]

    @api.onchange('test_commission_lines_ids.sub_total')
    def _onchange_compute_amount_total(self):
        """calculating commission amount"""
        for record in self:
            if record.test_commission_lines_ids:
                for rec in record.test_commission_lines_ids:
                    record.amount_total += rec.emp_commission
            else:
                record.amount_total = 0

    @api.onchange('commission_medicine_ids.amount_total_medicine')
    def compute_medicine_total(self):
        """calculating commission amount basis amount total"""
        for record in self:
            if record.commission_medicine_ids:
                for rec in record.commission_medicine_ids:
                    record.amount_total_medicine += rec.employ_commission_price
            else:
                record.amount_total_medicine = 0


class TestCommissionLines(models.Model):
    _name = 'test.commission.lines'
    _description = 'Test Commission lines'

    test_id = fields.Many2one('hospital.laboratory', string='Test')
    price = fields.Float('Price', related='test_id.price')
    test_commission_id = fields.Many2one('test.commission', string='Test')
    test_patient_id = fields.Many2one('patient.test')
    count = fields.Integer("Count")
    sub_total = fields.Float('Total', compute='_compute_total')
    commission = fields.Integer('Commission')
    emp_commission = fields.Float('Amount', compute='_compute_emp_commission')
    comm_price = fields.Integer()

    def _compute_emp_commission(self):
        for rec in self:
            if float(rec.comm_price) <= rec.sub_total:
                rec.emp_commission = rec.sub_total * float(rec.commission) / 100
            else:
                rec.emp_commission = 0.00

    def _compute_total(self):
        for rec in self:
            if rec.count:
                rec.sub_total = rec.price * float(rec.count)
            else:
                rec.sub_total = rec.price
