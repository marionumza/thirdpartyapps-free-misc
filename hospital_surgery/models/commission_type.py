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
from datetime import date
# from AptUrl.Helpers import _
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CommissionType(models.Model):
    _name = 'commission.type'
    _rec_name = 'commission_type_seq'

    employee_id = fields.Many2one('hr.employee')
    commission_as = fields.Selection(string='Commission as', selection=[('per', 'Percentage'), ('cash', 'Cash')],
                                     default='per', help='To select commission is given as cash or as percentage')
    commission_date = fields.Date("Date", default=date.today())
    expiry_date = fields.Date("Commission Expiry")
    commission_surgery_ids = fields.One2many('commission.surgery.line', 'surgery_commission_id')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('expired', 'Expired')], default='draft')

    commission_type_seq = fields.Char(string='Commission Number', required=True,
                                 copy=False, readonly=True, index=True,
                                 default=lambda self: 'New')

    @api.model
    def create(self, vals):
        if vals.get('commission_type_seq', 'New') == 'New':
            vals['commission_type_seq'] = self.env['ir.sequence'].next_by_code(
                'commission.type.sequence') or 'New'
        result = super(CommissionType, self).create(vals)
        return result

    def submit_button(self):
        """check the commission expired"""
        self.state = 'done'
        if self.commission_date < self.expiry_date:
            return
        else:
            raise ValidationError(_(
                "Check the Dates you Entered "
            ))


class CommissionSurgeryLines(models.Model):
    _name = 'commission.surgery.line'

    surgery_id = fields.Many2one('surgery.surgery','Surgery')
    amount = fields.Float("Price")
    commission_percentage = fields.Integer('Commission')
    comm_amount = fields.Float('Amount')
    surgery_commission_id = fields.Many2one('commission.type')

    @api.onchange('commission_percentage')
    def commission_amount(self):
        """calculating the commission in commission type"""
        if self.surgery_commission_id.commission_as == 'per':

            self.comm_amount = self.amount * (self.commission_percentage / 100)
        else:
            self.comm_amount = self.commission_percentage

