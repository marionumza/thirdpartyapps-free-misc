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


class Laboratory(models.Model):
    _name = 'hospital.laboratory'
    _description = 'Laboratory'
    _rec_name = "test_seq"

    test_name = fields.Char('Test')
    test_type = fields.Many2one('test.type', 'Test', required="True")
    date = fields.Date('Date')
    price = fields.Float(string='Price')
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    patient = fields.Many2one('res.partner', 'Patient')
    state = fields.Selection([('draft', 'Draft'), ('test', 'Test In Progress'),
                              ('complete', 'Complete'),
                              ('invoice', 'Invoiced'),
                              ],
                             string='State', readonly=True,
                             default="draft")
    interpretation = fields.Selection([('doctor', 'Deferred to doctor '),
                                       ('normal', 'Normal'),
                                       ('abnormal', 'Abnormal'),
                                       ('critical', 'Critical'),
                                       ('inconclusive', 'Inconclusive'),
                                       ('invalid', 'Invalid'),
                                       ], string="Result Interpretation", help="Patient Condition")
    info = fields.Text(string='Additional Information')
    previous = fields.Text(string='Previous Result Interpretation', help="Previous interpretation")
    test_seq = fields.Char(string='Test Sequence', required=True,
                           copy=False,
                           readonly=True,
                           index=True,
                           default=lambda self: 'New')
    hos_lab_ids = fields.One2many('lab.test.result', 'lab_result_id',
                                  string="Lab ID")

    notes = fields.Text('notes')
    lab_ids = fields.Many2many('hospital.labs')
    type_name = fields.Char('Nature', related='test_type.type_name')
    invoice_id = fields.Many2one('account.move')

    def lab_button(self):
        self.state = 'test'

    def lab_button_end(self):
        self.state = 'complete'

    def lab_button_payment(self):
        self.state = 'invoice'
        inv_line_list = []
        for rec in self:
            inv_line = (0, 0, {'name': rec.patient.name,
                               'price_unit': self.price,
                               })
            inv_line_list.append(inv_line)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'invoice_date': fields.Date.today(),
            'partner_id': self.patient.id,
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
        if vals.get('test_seq', 'New') == 'New':
            vals['test_seq'] = self.env['ir.sequence'].next_by_code(
                'test.sequence') or 'New'
        result = super(Laboratory, self).create(vals)
        return result


class TestResult(models.Model):
    _name = 'lab.test.result'
    _description = ' Test Result'

    test_sub_id = fields.Many2one('test.test')
    patient_id = fields.Many2one('res.partner')
    result = fields.Float()
    normal = fields.Float(help="The normal rate of the test")
    unit = fields.Char()
    lab_result_id = fields.Many2one('hospital.laboratory', string="Test ID")


class TestTest(models.Model):
    _name = 'test.test'
    _rec_name = 'test_name'

    test_name = fields.Char('Test')
    test_type = fields.Many2one('test.type', 'Test Type', required="True")
    price = fields.Float('Price')