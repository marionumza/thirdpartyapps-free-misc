 #-*- coding: utf-8 -*-
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
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CommissionConfig(models.Model):
    _name = 'commission.configuration'
    _rec_name = 'commission_seq'
    _description = 'Commission Configuration'

    employee_id = fields.Many2one('hr.employee')
    commission_type = fields.Selection([('test', 'Test'), ('medicine', 'Medicine')],
                                       string='Type', default='test', required=True)
    note = fields.Text('Note')
    commission_ids = fields.One2many('commission.configurations.lines', 'commission_id', "Commission Lines")
    commission_test_ids = fields.One2many('commission.test.lines', 'commission_test_id', "Commission Lines")
    commission_as = fields.Selection(string='Commission as', selection=[('per', 'Percentage'), ('cash', 'Cash')],
                                     default='per', help='To select commission is given as cash or as percentage')
    amount_total = fields.Monetary('Total', compute='compute_amount_total')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    commission_seq = fields.Char(string='Commission Code', required=True,
                                 copy=False, readonly=True, index=True,
                                 default=lambda self: 'New')
    commission_date = fields.Date("Date", default=date.today())
    expiry_date = fields.Date("Commission Expiry")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('expired', 'Expired')], default='draft')

    @api.model
    def create(self, vals):
        if vals.get('commission_seq', 'New') == 'New':
            vals['commission_seq'] = self.env['ir.sequence'].next_by_code(
                'hospital.commission') or 'New'
        result = super(CommissionConfig, self).create(vals)
        return result

    def submit_button(self):
        """checking the commission expires or not"""
        self.state = 'done'
        if self.commission_date < self.expiry_date:
            return
        else:
            raise ValidationError(_(
                "Check the Dates you Entered "
            ))


class CommissionConfigLines(models.Model):
    _name = 'commission.configurations.lines'
    _description = 'Commission Configuration Lines'

    product_ids = fields.Many2one('hospital.medicine', string=' Medicine')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    price = fields.Monetary('Price')
    count = fields.Integer("Count")
    comm_price = fields.Integer('ToTal Price', compute='_onchange_compute_amount_total')
    product_price = fields.Monetary('Unit Price', related='product_ids.price')
    amount = fields.Monetary('Amount', compute='compute_amount')
    medi_commission_id = fields.Many2one('test.commission')
    commission_id = fields.Many2one('commission.configuration', 'Amount')
    commission_percentage = fields.Integer('Commission')
    employ_commission_price = fields. Float('Amount', compute='_compute_commission_price')

    def compute_amount(self):
        """compute the commission  amount while commission is percentage"""
        for rec in self:
            rec.amount = rec .price * rec. commission_percentage /100

    def _compute_commission_price(self):
        """compute the commission  amount while commission is price"""
        for rec in self:
            if float(rec.comm_price) >= rec.amount:
                rec .employ_commission_price = rec.comm_price * float(rec.commission_percentage) / 100

            else :
                rec.employ_commission_price = 0.00

    def _onchange_compute_amount_total(self):
        """compute total commission basis of no.of medicine/tests"""
        for record in self:
            record.comm_price = record.count * record.product_price

    @api.onchange('commission_percentage')
    def onchange_commission_amount(self):
        """compute the commission  amount while commission is percentage"""
        if self.commission_id.commission_as == 'per':
            self.amount = self.price * (self.commission_percentage / 100)
        else:
            self.amount = self.price + self.commission_percentage


class CommissionMedicineLines(models.Model):
    _name = 'commission.test.lines'
    _description = 'Commission Configuration Lines'

    doctor_ids = fields.Many2one('hr.employee', string="Doctor", domain="[('is_doctor','=','doctor')]")
    product_ids = fields.Many2one('hospital.laboratory', string='Test', help="laboratory tests" )
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    price = fields.Monetary('Price')
    commission_percentage = fields.Integer('Commission',help="The percentage that is for total amount")
    amount = fields.Monetary('Amount')
    commission_test_id = fields.Many2one('commission.configuration')
    commission_as = fields.Selection(string='Designation', selection=[('per', 'Percentage'), ('cash', 'Cash')],
                                     default='per', help='To select commission is given as cash or as percentage')

    @api.onchange('commission_percentage')
    def commission_amount(self):
        """computing the commission amount"""
        if self.commission_test_id.commission_as == 'per':

            self.amount = self.price * (self.commission_percentage / 100)
        else:
            self.amount = self.commission_percentage
