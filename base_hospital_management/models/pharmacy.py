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
from odoo import models, fields, api


class Pharmacy(models.Model):
    _name = 'hospital.pharmacy'
    _description = 'Pharmacy'
    _rec_name = 'pharmacy_name'

    pharmacy_name = fields.Char(string="Pharmacy Name", required="True")
    pharmacist_name = fields.Many2one('hr.employee', string="Pharmacist's Name",
                                      domain=[('job_title', '=', 'Pharmacist')])
    health_center = fields.Many2one("hospital.hospital", 'Health Center')
    phone = fields.Char(' Phone')
    mobile = fields.Char(' Mobile')
    email = fields.Char(' Email')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    prescription_ids = fields.One2many('hospital.prescription', 'pharmacy_id', "Prescription")
    doctor_ids = fields.One2many('hr.employee', 'pharmacy_id', "Prescription")
    notes = fields.Text('Notes')
    doctor_id = fields.Many2one('hr.employee', 'Doctor')
    image_129 = fields.Image(max_width=128, max_height=128)
    doctor_name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    user_partner_id = fields.Many2one(related='user_id.partner_id', related_sudo=False, string="User's partner")
    user_id = fields.Many2one('res.users', string="Responsible")

    @api.constrains('prescription_ids')
    @api.onchange('prescription_ids')
    def onchange_medicine(self):
        for rec in self.prescription_ids:
            vals = []
            if rec.pharmacy_id and rec.medicine_id:
                vals.append((0, 0, {'prescription_id': rec.id,
                                    'medicine_id': rec.medicine_id.id}))
                rec.prescription_ids = vals


class Prescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Prescription'
    _rec_name = 'prescription_seq'

    patient_id = fields.Many2one('res.partner', 'Patient')
    patient_name = fields.Char('Name', related='patient_id.name')
    dob = fields.Date('Date of Birth', related='patient_id.dob')
    gender = fields.Selection('Gender', related='patient_id.gender')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    phone = fields.Char('Phone No.', related='patient_id.phone')
    mobile = fields.Char('Mobile No.', related='patient_id.mobile')
    email = fields.Char('Email', related='patient_id.email')
    doctor_id = fields.Many2one('hr.employee', 'Doctor')
    total = fields.Integer("Total")
    medicine_id = fields.Many2one('hospital.medicine', string="Medicine")
    pharmacy_id = fields.Many2one('hospital.pharmacy', string="Pharmacy", required=True)
    diagnosis_id = fields.Many2one('hospital.diagnosis', string="Diagnosis")
    prescription_seq = fields.Char(string='Prescription Sequence', required=True, copy=False, readonly=True, index=True,
                                   default=lambda self: 'New')
    unit_price = fields.Monetary("Unit Price",related = 'medicine_id.price')
    prescription_ids = fields.One2many('hospital.prescription.lines', 'prescription_id')
    payment_id = fields.Many2one('hospital.payment', "Payment ")
    amount_total = fields.Monetary('Total', compute='_onchange_compute_amount_total')

    prescription_date = fields.Datetime('Date', default=fields.Datetime.now)
    dose = fields.Char('Dosage', help="Dosage of the medicine")
    days = fields.Integer('Days', help="the no:of dys to be taken the medicine")
    invoice_id = fields.Many2one('account.move')
    payment_state = fields.Selection([('paid', 'Paid'), ('not_paid', 'Partial'),
                                      ('in_payment', 'In Payment')],
                                     default='not_paid')
    bool = fields.Boolean(default=False)

    test_name = fields.Char('Test')
    price = fields.Float(string='Price')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    notes = fields.Text('notes')
    lab_ids = fields.Many2many('hospital.labs')
    test_type = fields.Many2one('test.type', "Test Type")
    type_name = fields.Char('Nature')

    @api.onchange('prescription_ids.sub_total')
    def _onchange_compute_amount_total(self):
        """amount n the prescription is calculated"""
        for record in self:
            if record.prescription_ids:
                for rec in record.prescription_ids:
                    record.amount_total += rec.sub_total
            else:
                record.amount_total = 0

    @api.model
    def create(self, vals):
        if vals.get('prescription_seq', 'New') == 'New':
            vals['prescription_seq'] = self.env['ir.sequence'].next_by_code(
                'prescription.sequence') or 'New'
        result = super(Prescription, self).create(vals)
        return result

    def action_payment(self):
        """"payment methode"""
        self.bool = True
        inv_line_list = []
        for rec in self.prescription_ids:
            inv_line = (0, 0, {'name': rec.medicine_id.medicine,
                               'price_unit': rec.unit_price,
                               'quantity': rec.quantity,
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


class PrescriptionLines(models.Model):
    _name = 'hospital.prescription.lines'
    _description = 'Prescription Lines'
    _rec_name = 'prescription_id'

    medicine_id = fields.Many2one('hospital.medicine', 'Medicine')
    unit_price = fields.Monetary("Unit Price",related = 'medicine_id.price')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    count = fields.Integer("Count")
    commission = fields. Integer('Commission', help="commission basis of medicine in the pharmacy")
    quantity = fields.Integer('Quantity', help="The no:of medicines for the time period")
    sub_total = fields.Monetary('Sub-Total')
    no_intakes = fields.Integer('Intakes', help="How much medicine want to take")
    time = fields.Selection([('once', 'Once in a day'), ('twice', 'Twice in a Day'),
                             ('thrice', 'Thrice in a day'), ('morning', 'In Morning'),
                             ('noon', 'In Noon'), ('evening', 'In Evening')])
    prescription_id = fields.Many2one('hospital.prescription', 'Prescription')
    payment_id = fields.Many2one('account.payment', 'Payment')

    @api.onchange('quantity')
    def onchange_sub_total(self):
        """subtotal of medicine basis of quantity"""
        for rec in self:
            rec.sub_total = rec.quantity * rec.unit_price


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_register_payment(self):
        res = super(AccountMove, self).action_register_payment()
        self.env['hospital.prescription'].search(
            [('invoice_id', '=', self.id)]).write(
            {'payment_state': 'paid'})
        return res
