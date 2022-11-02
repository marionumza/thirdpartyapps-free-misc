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
from datetime import date
import json


class LabResult(models.Model):
    _name = 'lab.result'
    _description = 'Lab Result'
    _rec_name = 'result_seq'

    result_seq = fields.Char(string='Result No.', required=True,
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
    test_date = fields.Date('Date', required=True, default=date.today())
    date_today = date.today()
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    test_id = fields.Many2one('hospital.laboratory', 'Test')
    test_result_ids = fields.One2many('test.result', 'result_id', "Result Lines")
    test_result_second_ids = fields.One2many('test.result.second', 'result_id', "Result Lines")
    type_id = fields.Many2one('test.type', 'Test Type ', help="Select type according to your test.")
    test_type = fields.Selection('Test Nature', related='type_id.test_type', default='range')

    @api.model
    def create(self, vals):
        if vals.get('result_seq', 'New') == 'New':
            vals['result_seq'] = self.env['ir.sequence'].next_by_code(
                'result.sequence') or 'New'
        result = super(LabResult, self).create(vals)
        return result


class TestFirst(models.Model):
    _name = 'test.result'
    _description = 'Test Result'

    result_id = fields.Many2one('lab.result', 'Result ID')
    observation = fields.Integer('Observation')
    normal = fields.Integer('Normal Range')
    units = fields.Char('Unit')
    result = fields.Integer('Result')
    lab_id = fields.Many2one('hospital.labs')
    test_id = fields.Many2one('hospital.laboratory', 'Test', required=True)
    test_domain_id = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=False,
    )

    @api.depends('result_id.type_id')
    def _compute_product_id_domain(self):

        for rec in self:
            print(rec.result_id.type_id,'rec')
            # rec.test_domain_id = self.env['hospital.laboratory'].search([('test_type','=',rec.result_id.type_id.id)])
            # print(val,'fgvuygyuvh')
            # # tests = []
            # for ric in val:
            #     print(ric.test_name)
            rec.test_domain_id = json.dumps([('test_type','=',rec.result_id.type_id.id)])
                # tests.append(rec)
            # print(tests)
            # return tests


    # def _default_test(self):
    #     print(self,'self')
    #     print(self.result_id, 'hniuhuhbhu buy')
    # val = self.env['hospital.laboratory'].search([('test_type', '=', self.result_id.type_id)])
    # print(val, 'valll')


class TestSecond(models.Model):
    _name = 'test.result.second'
    _description = 'Test Result'

    result_id = fields.Many2one('lab.result', 'Result ID')
    select_result = fields.Selection([('Infected', 'Infected'), ('Not-Infected', 'Not-Infected')], 'Result')
    remarks = fields.Text('Remarks')
    name = fields.Text('Name')
