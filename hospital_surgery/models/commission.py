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
from odoo import fields, models, api
from odoo.fields import Date


class SurgeryCommission(models.Model):
    _name = 'surgery.commission'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee')
    employee_commission = fields.Many2one('commission.type', 'Commission')
    date = fields.Date('Date', default=Date.today())
    surgery_id_commission = fields.One2many('hospital.surgery.line', 'test_surgery_id')

    @api.onchange('employee_commission')
    def onchange_employee_commission_surgery(self):
        for rec in self:
            a = self.env['commission.type'].search(
                [('employee_id', '=', rec.employee_id.id)])
            rec.surgery_id_commission = [(5, 0, 0)]
            for line in a.commission_surgery_ids:
                vals = {
                    'surgery_id': line.surgery_id.id,
                    'commission_surgery': line.commission_percentage,
                    'comm_price': line.amount,
                    'count': self.env['surgery.payment'].search_count([('surgery_id', '=', line.surgery_id.id)]),
                }
                zxc=self.env['surgery.payment'].search_count([('surgery_id', '=', line.surgery_id.id)])
                rec.surgery_id_commission = [(0, 0, vals)]


class SurgeryCommissionLine(models.Model):
    _name = 'hospital.surgery.line'

    surgery_id = fields.Many2one('surgery.surgery', 'Surgery')
    sur_amount = fields.Float('Uprice', related='surgery_id.sur_amount')
    comm_price = fields.Float('Comm Price')
    count = fields.Integer('Count')
    commission_surgery = fields.Float('Commission')
    tot_amount_surgery = fields.Float('Tot Amt', compute='compute_total_surgery_amt')
    tot_commission = fields.Float('Amount', compute='tot_surgery_commission')
    test_surgery_id = fields.Many2one('surgery.commission')

    def compute_total_surgery_amt(self):
        """commission for surgery count calculated """
        for rec in self:
            if rec.count:
                rec.tot_amount_surgery = rec.sur_amount * float(rec.count)
            else:
                rec.tot_amount_surgery = rec.sur_amount

    def tot_surgery_commission(self):
        """commission for surgery calculated """
        for rec in self:
            if float(rec.comm_price) <= rec.tot_amount_surgery:
                rec.tot_commission = rec.tot_amount_surgery * float(rec.commission_surgery) / 100
            else:
                rec.tot_commission = 0.00
