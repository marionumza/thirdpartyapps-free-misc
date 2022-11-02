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


class SurgeryPayment(models.Model):
    _name = 'surgery.payment'
    _rec_name = 'patient_name'

    payment_seq = fields.Char(string='Surgery Number', required=True, copy=False, readonly=True, index=True,
                              default=lambda self: 'New')
    patient_id = fields.Many2one('res.partner', string="Patient Name", required=True)
    patient_name = fields.Char("Patient Name", related='patient_id.name')
    dob = fields.Date(string="Date of Birth", related='patient_id.dob')
    gender = fields.Selection([('female', 'Female'),
                               ('male', 'Male'),
                               ('others', 'Other')],
                              string="Gender", related='patient_id.gender')
    patient_age = fields.Integer(string="Age", related='patient_id.patient_age')
    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid'), ('cancel', 'Cancelled'), ('done', 'Done'),
                              ], default='draft')
    hosp_date = fields.Date(string="Hospitalization Date")
    discharge_date = fields.Date(string="Discharge Date")
    payment_surgery_id = fields.One2many('surgery.payment.line', 'surgery_payment_id')
    amount_total_surgery = fields.Monetary('Total Price')
    invoice_id = fields.Many2one('account.move')
    surgery_id = fields.Many2one('surgery.surgery', 'Surgery')

    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id)

    @api.onchange('surgery_id')
    def surgery_payment(self):
        for rec in self:
            val = self.env['surgery.surgery'].search([('name','=',rec.surgery_id.name)])
            rec.payment_surgery_id = [(5, 0, 0)]
            for line in val.surgery_equipment_id:
                vals = {
                    'surgery_id': line.name_id,
                    'amount': line.standard_price,
                    'surgery_cat_id': val.sur_cat,
                }
                rec.payment_surgery_id = [(0, 0, vals)]

    def surgery_invoice(self):
        inv_line_list = []
        for rec in self.payment_surgery_id:
            inv_line = (0, 0, {
                               'product_id': rec.surgery_id,
                               'name': rec.surgeon_id.name,
                               'price_unit': rec.amount,
                               })
            inv_line_list.append(inv_line)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'invoice_date': fields.Date.today(),
            'partner_id': self.patient_id.id,
            'invoice_line_ids': inv_line_list
        })
        self.invoice_id = invoice.id
        return {
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_Id': self.env.ref('account.view_move_form').id,
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': invoice.id
        }

    @api.model
    def create(self, vals):
        if vals.get('payment_seq', 'New') == 'New':
            vals['payment_seq'] = self.env['ir.sequence'].next_by_code(
                'payment.sequence') or 'New'
        result = super(SurgeryPayment, self).create(vals)
        return result


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_register_payment(self):
        res = super(AccountMove, self).action_register_payment()
        self.env['surgery.payment'].search(
            [('invoice_id', '=', self.id)]).write(
            {'state': 'paid'})
        return res


class SurgeryPaymentLine(models.Model):
    _name = 'surgery.payment.line'

    surgeon_id = fields.Many2one('hr.employee', string="Surgeon", domain="[('is_doctor','=','doctor')]")
    surgery_cat_id = fields.Many2one('surgery.type', 'Surgery Category')
    surgery_id = fields.Many2one('product.product', 'Surgery')
    surgery_payment_id = fields.Many2one('surgery.payment')
    patient_id = fields.Many2one('res.partner', string="Patient Name")
    amount = fields.Float("Amount")
