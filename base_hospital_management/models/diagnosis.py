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


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnosis'
    _rec_name = 'diagnosis_seq'

    patient_name = fields.Char('Name', related='patient_seq_id.name')
    dob = fields.Date('Date of Birth', related='patient_seq_id.dob')
    diagnosis_date = fields.Datetime('Date', default=fields.Datetime.now,
                                     help="The date which is the doctor consulting the patient")
    diagnosis_type = fields.Selection([
        ('home', 'Home Consultancy'),
        ('telephone', 'Telephone Consultancy'),
        ('hospital', 'Hospital Consultancy'),
        ('nursing', 'Nursing-Home Consultancy'),
        ('clinic', 'Clinic Consultancy'),
        ('community', 'Community-Health Center Consultancy'),
        ('other', 'Other')],
        string="Mode of diagnosis")
    gender = fields.Selection('Gender', related='patient_seq_id.gender')
    patient_age = fields.Integer('Age', related='patient_seq_id.patient_age')
    phone = fields.Char('Phone No.', related='patient_seq_id.phone')
    mobile = fields.Char('Mobile No.', related='patient_seq_id.mobile')
    email = fields.Char('Email', related='patient_seq_id.email')
    diagnosis_seq = fields.Char(string='SI No', required=True, copy=False,
                                readonly=True, index=True,
                                default=lambda self: 'New')
    patient_seq_id = fields.Many2one('res.partner', 'Patient Code')
    note = fields.Html('Note', sanitize_style=True)
    prescription_ids = fields.One2many('hospital.prescription', 'diagnosis_id', "Prescription")
    diagnosis_count = fields.Integer(string="Count", compute="_compute_count" ,help="Total no:of consultation")
    payment_state = fields.Selection([('paid', 'Paid'), ('not_paid', 'Partial'),
                                      ('in_payment', 'In Payment')],
                                     default='not_paid')

    @api.constrains('prescription_ids')
    @api.onchange('prescription_ids')
    def onchange_medicine(self):
        """creating medicines in prescription"""
        vals = []
        for rec in self.prescription_ids:

            if rec.pharmacy_id and rec.medicine_id:

                vals.append((0, 0, {'prescription_id': rec.id,
                                    'medicine_id': rec.medicine_id.id}))
                vals.append(vals)
            rec.prescription_ids = vals

    @api.model
    def create(self, vals):
        if vals.get('diagnosis_seq', 'New') == 'New':
            vals['diagnosis_seq'] = self.env['ir.sequence'].next_by_code(
                'patients.diagnosis') or 'New'
        result = super(Diagnosis, self).create(vals)
        return result
