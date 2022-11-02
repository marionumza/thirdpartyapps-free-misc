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
import datetime


class Patient(models.Model):
    _name = 'hospital.inpatient'
    _description = 'Patient'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', string="Patient Name", required=True)
    patient_name = fields.Char("Patient Name", related='patient_id.name')
    reason = fields.Char(string="Reason for Admission", help="Current reason for hospitalization of the patient")
    building_id = fields.Many2one('hospital.buildings', string="Block Name",
                                  required=True)
    ward_id = fields.Many2one('hospital.wards', string='Ward')
    bed_id = fields.Many2one('hospital.beds', string='Bed')
    room_no = fields.Many2one('patient.room')
    type_admission = fields.Selection([('emergency', 'Emergency Admission'),
                                       ('routine', 'Routine Admission')],
                                      string="Admission Type", required=True)
    attending_doctor = fields.Many2one('hr.employee',string="Attending Doctor", domain="[('is_doctor','=','doctor')]")
    operating_doctor = fields.Many2one('hr.employee',string="Operating Doctor", domain="[('is_doctor','=','doctor')]")
    hosp_date = fields.Date(string="Hospitalization Date", required=True)
    discharge_date = fields.Date(string="Discharge Date")
    condition = fields.Text(string="Condition Before Hospitalization",
                            help="The condition of the patient while he/she is admitted to the hospital")
    nursing_plan = fields.Text(string="Nursing Plan")
    discharge_plan = fields.Text(string="Discharge Plan")
    notes = fields.Text(string="Notes ")
    pvt_rooms = fields.Boolean("Private Rooms")
    room_id = fields.Many2one('patient.room', string='Rooms')
    room_rent = fields.Monetary(string='Rent', related='room_id.rent')
    bed_rent = fields.Monetary(string='Rent', related='bed_id.bed_rent')
    facilities_ids = fields.Many2many(string='Facilities', related='room_id.facilities_ids')
    ward_facilities_ids = fields.Many2many(string='Facilities', related='ward_id.facilities')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    state = fields.Selection([('draft', 'Draft'), ('reserve', 'Reserved'),
                              ('Admit', 'Admitted'), ('invoice', 'Invoiced'), ('dis', 'Discharge')],
                             string='State', readonly=True,
                             default="draft")
    rent_amount = fields.Monetary(string="Rent Amount", compute='_compute_amount')
    bed_rent_amount = fields.Monetary(string="Rent Amount", compute='_bed_compute_amount')
    days = fields.Integer(string='Days')
    invoice_id = fields.Many2one('account.move')
    admit_days = fields.Integer(string='Days', compute='_compute_days')

    @api.onchange('bed_id')
    def onchange_bed(self):
        """"unassigned the beds"""
        val = self.env['hospital.beds'].search([('id', '=', self.bed_id.id)])
        for rec in val:
            rec.write({
                'state': 'not'
            })

    @api.onchange('discharge_date')
    def onchange_discharge(self):
        """"assigned the beds"""
        val = self.env['hospital.beds'].search([('id','=',self.bed_id.id)])
        if val.date_bed_assign < self.discharge_date:
            for rec in val:
                rec.write({
                    'state': 'avail'
                })
        else:
            for rec in val:
                rec.write({
                    'state': 'not'
                })

    def action_invoice(self):
        self.state = 'invoice'

        inv_line_list = []
        for rec in self:
            inv_line = (0, 0, {'name': rec.patient_id.name,
                               'price_unit': rec.bed_rent_amount,
                               'quantity': rec.admit_days,
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

    def _compute_days(self):
        if self.hosp_date:
            if self.discharge_date:
                self.admit_days = (self.discharge_date - self.hosp_date +
                                   datetime.timedelta(days=1)).days
            else:
                self.admit_days = (fields.date.today() - self.hosp_date +
                                   datetime.timedelta(days=1)).days

    def _compute_amount(self):
        if self.hosp_date:
            if self.discharge_date:
                self.days = (self.discharge_date - self.hosp_date +
                             datetime.timedelta(days=1)).days
                self.rent_amount = self.room_id.rent * self.days
            else:
                self.days = (fields.date.today() - self.hosp_date +
                             datetime.timedelta(days=1)).days
                self.rent_amount = self.room_id.rent * self.days
        else:
            self.rent_amount = self.room_id.rent

    def _bed_compute_amount(self):
        if self.hosp_date:
            if self.discharge_date:
                self.days = (self.discharge_date - self.hosp_date +
                             datetime.timedelta(days=1)).days
                self.bed_rent_amount = self.bed_id.bed_rent * self.days
            else:
                self.days = (fields.date.today() - self.hosp_date +
                             datetime.timedelta(days=1)).days
                self.bed_rent_amount = self.bed_id.bed_rent * self.days
        else:
            self.bed_rent_amount = self.bed_id.bed_rent

    def action_admit(self):
        self.state = 'Admit'
        self.bed_id.state = "not"
        self.room_id.state = "not"

    def action_reserve(self):
        self.state = 'reserve'
        self.room_id.state = 'reserve'

    def action_discharge(self):
        self.state = 'dis'
        self.bed_id.state = "avail"
        self.room_id.state = 'avail'

    @api.onchange('building_id')
    def _onchange_ward(self):
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    @api.onchange('ward_id')
    def _onchange_ward_beds(self):
        return {'domain': {
            'bed_id': [
                ('ward_id', '=', self.ward_id.id),
                ('state', '=', 'avail')
            ]}}

    @api.onchange('ward_id')
    def _onchange_ward_rooms(self):
        return {'domain': {
            'room_id': [
                ('ward_id', '=', self.ward_id.id),
                ('state', '=', 'avail')

            ]}}
