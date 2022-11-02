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


class TestAppointments(models.Model):
    _name = 'test.appointment'
    _description = 'Lab'
    _rec_name = 'appoint_seq'

    appoint_seq = fields.Char(string='Appointment No.', required=True,
                              copy=False,
                              readonly=True,
                              index=True,
                              default=lambda self: 'New')
    patient_seq_id = fields.Many2one("res.partner", 'Patient No.')
    patient_name = fields.Char('Name', related='patient_seq_id.name')
    dob = fields.Date('Date of Birth', related='patient_seq_id.dob')
    gender = fields.Selection('Gender', related='patient_seq_id.gender')
    patient_age = fields.Integer('Age', related='patient_seq_id.patient_age')
    phone = fields.Char('Phone No.', related='patient_seq_id.phone')
    mobile = fields.Char('Mobile No.', related='patient_seq_id.mobile')
    email = fields.Char('Email', related='patient_seq_id.email')
    appointment_date = fields.Date('Appointment Date')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    test_type = fields.Many2one('test.type')
    # patient_test_ids = fields.One2many('patient.test', 'appointment_id', "Tests")
    state = fields.Selection(
        [('draft', "Draft"), ('start', "Start Test"), ('end', 'End Test'), ('cancel', 'Cancelled')],
        default='draft')
    lab_technician = fields.Many2one('lab Technician')
    payment_state = fields.Selection([('paid', 'Paid'), ('not_paid', 'Partial'),
                                      ('in_payment', 'In Payment')],
                                     compute='_compute_payment_state')
    invoice_id = fields.Many2one('account.move')
    doctor_id = fields.Many2one('hr.employee', string="Doctor", domain="[("
                                                                       "'is_doctor','=','doctor')]", )
    inverse_id = fields.Many2one('res.partner')
    bool = fields.Boolean(default=False)
    payment_status = fields.Char()
    price = fields.Float('Price')

    def _compute_payment_state(self):
        """payment state computation"""
        for rec in self:
            rec.payment_state = rec.invoice_id.payment_state

    @api.model
    def create(self, vals):
        if vals.get('appoint_seq', 'New') == 'New':
            vals['appoint_seq'] = self.env['ir.sequence'].next_by_code(
                'appoint.sequence') or 'New'
        result = super(TestAppointments, self).create(vals)
        return result

    def action_start(self):
        self.env['lab.result'].sudo().create({
            'patient_seq_id': self.patient_seq_id.id,
            'patient_name': self.patient_name,
            'dob': self.dob,
            'gender': self.gender,
            'patient_age': self.patient_age,
            # 'email': self.email,
            'type_id': self.test_type.id,
        })
        self.state = 'start'


    def action_payment(self):
        # self.bool = True
        inv_line_list = []
        for rec in self:
            inv_line = (0, 0, {
                               'name': rec.test_type.type_name,
                               'price_unit': rec.price,

                               })
            inv_line_list.append(inv_line)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'invoice_date': fields.Date.today(),
            'partner_id': self.patient_seq_id.id,
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

    def action_end(self):
        self.state = 'end'

    def action_cancel(self):
        self.state = 'cancel'


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_register_payment(self):
        res = super(AccountMove, self).action_register_payment()
        self.env['test.appointment'].search(
            [('invoice_id', '=', self.id)]).write(
            {'payment_status': 'paid'})
        return res

# class PatientTest(models.Model):
#     _name = 'patient.test'
#     _description = 'Patient test'
#
#     test_id = fields.Many2one('hospital.laboratory', string='Test')
#     price = fields.Float('Price', related='test_id.price')
#     lab_ids = fields.Many2one('hospital.labs')
#     lab_name = fields.Char('Name', related='lab_ids.name')
#     appointment_id = fields.Many2one('test.appointment', 'Appointment')
#     currency_id = fields.Many2one('res.currency', 'Currency',
#                                   default=lambda self: self.env.user.company_id
#                                   .currency_id.id,
#                                   required=True)
#     result_id = fields.Many2one('lab.result', 'Result', help="result of the test")
#     patient_seq_id = fields.Many2one("res.partner", 'Patient No.')
#     patient_name = fields.Char('Name', related='patient_seq_id.name')
#     pat_name = fields.Char("Name", compute='_compute_name')
#     dob = fields.Date('Date of Birth', related='patient_seq_id.dob')
#     gender = fields.Selection('Gender', related='patient_seq_id.gender')
#     patient_age = fields.Integer('Age', related='patient_seq_id.patient_age')
#     email = fields.Char('Email', related='patient_seq_id.email')
#     payment_id = fields.Many2one('test.appointment',
#                                  string="Payment ID", help="payment for the test")
#     doctor_id = fields.Many2one('hr.employee', compute='_compute_doctor_id')
#     appoint_date = fields.Date('Date', related='appointment_id.appointment_date')
#
#     def _compute_doctor_id(self):
#         """The available doctors are taken"""
#         for rec in self:
#             rec.doctor_id = rec.appointment_id.doctor_id.id
#
#     def _compute_name(self):
#         for rec in self:
#             rec.pat_name = rec.appointment_id.patient_name
