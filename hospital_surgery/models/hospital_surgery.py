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
from datetime import date, timedelta
# from AptUrl.Helpers import _
from werkzeug import urls
from odoo import fields, models, api, _
from odoo.fields import Date


class HospitalSurgery(models.Model):
    _name = 'hospital.surgery'
    _rec_name = "surgery_seq"

    surgery_seq = fields.Char(string='Surgery Number', required=True, copy=False, readonly=True, index=True,
                              default=lambda self: 'New')

    patient_id = fields.Many2one('res.partner', string="Patient Code", required=True)
    patient_name = fields.Char("Patient Name", related='patient_id.name')
    dob = fields.Date(string="Date of Birth", required=True,related='')
    gender = fields.Selection([('female', 'Female'),
                               ('male', 'Male'),
                               ('others', 'Other')],
                              string="Gender", required=True)
    patient_age = fields.Integer(string="Age", compute='_compute_age')
    type_admission = fields.Selection([('emergency', 'Emergency Admission'),
                                       ('routine', 'Routine Admission')],
                                      string="Admission Type", required=True)
    surgeon_id = fields.Many2one('hr.employee', string="Surgeon", domain="[('is_doctor','=','doctor')]")
    building_id = fields.Many2one('hospital.buildings', string="Block Name",
                                  required=True)
    hosp_date = fields.Date(string="Hospitalization Date", required=True)
    discharge_date = fields.Date(string="Discharge Date")
    condition = fields.Text(string="Condition before hospitalization")
    notes = fields.Text(string="Notes ")
    op_theater_id = fields.Many2one('hospital.operation', 'Operation Theater')
    surgery_cat_id = fields.Many2one('surgery.type', 'Surgery Category', help="Surgery Category")
    surgery_id = fields.Many2one('surgery.surgery', 'Surgery')
    anesthesist_id = fields.Many2one('hr.employee', string="Anaesthetist", domain="[('is_doctor','=','doctor')]")
    nurse_anesthetist = fields.Many2one('hr.employee', string="Nurse Anaesthetist")
    circulating_nurse = fields.Many2one('hr.employee', string="Circulating Nurse")
    surgical_technologist = fields.Many2one('hr.employee', string="Surgical Technologist")
    signed_by = fields.Char('Signed By')
    relation = fields.Char('Relation')
    primary_insurance = fields.Many2one('hospital.insurance')
    insurance_id = fields.Char('Insurance Id')
    group = fields.Char()
    goup_policy_emp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    govt_policy_emp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    policy_holder_name = fields.Char('Policy Holder Name')
    policy_holder_dob = fields.Date('Policy Holder Dob')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('inprogress', 'In progress'), ('done', 'Done'),
         ('cancel', 'Cancelled')], default='draft')
    patient_identification = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                              help='The nurse will ask patient '
                                                   'complete name and birthday, '
                                                   'check patient '
                                                   'identification '
                                                   'bracelet and compare it '
                                                   'against your record')
    surgical_consent = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                        help='The nurse may witness patient '
                                             'signature on patient written '
                                             'surgical '
                                             ' consent. You are encouraged to '
                                             'ask questions about your surgery')

    history_physical_examination = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                                    help='Your surgeon will '
                                                         'completely document '
                                                         'your medical history '
                                                         'and physical '
                                                         'examination.')
    surgical_site_signature = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                               help='Surgical site signature '
                                                    'means your surgeon or '
                                                    'designee will sign the '
                                                    'site of your surgery to '
                                                    'accurately identify the '
                                                    'area of your surgery. Not '
                                                    'everybody will have this '
                                                    'surgical site signature. '
                                                    'The need for surgical '
                                                    'site signature is for '
                                                    'patients with surgery '
                                                    'that indicates a right or '
                                                    'left location, For '
                                                    'example: left leg, '
                                                    'right arm, left eye, '
                                                    'or right kidney.')
    blood_specimen = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                      help='check the patient identification and compare it against the blood label '
                                           'to make sure there is a correct match.')
    x_ray = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                             help='If you bring an x-ray film with you, the nurse will check if the label matches '
                                  'correctly with your identification.')
    anesthesia_interview = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                            help='Your anesthesiologist will interview you before surgery')

    list_medications = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Reject')],
                                        help='Make sure you bring your list of '
                                             'medications, doses and how often '
                                             'you take them. The medications '
                                             'will include both prescribed and '
                                             'over the counter medications, '
                                             'herbs and other medications like '
                                             'cocaine. The nurse will validate '
                                             'all of these medications on the '
                                             'day of surgery.')
    allergy = fields.Selection(
        [('itchiness', 'Itchiness'), ('redness', 'Redness'), ('hives', 'Hives'), ('other', 'Other')],
        help='Your anesthesiologist will interview you before surgery')
    other_allergy = fields.Char()
    next_appointment = fields.Date('Next Appointment Date')

    def confirm_surgery(self):
        """Reserving the operation theater when confirming the surgery"""
        self.state = 'confirm'
        val = self.env['hospital.operation'].search([('id', '=', self.op_theater_id.id)])
        for rec in val:
            rec.write({
                'state': 'reserved'
            })

    def start_surgery(self):
        """When the operation theater Occupied"""
        self.state = 'inprogress'
        val = self.env['hospital.operation'].search([('id', '=', self.op_theater_id.id)])
        for rec in val:
            rec.write({
                'state': 'occupied'
            })

    def complete_surgery(self):
        """operation theater is free after completed the surgery"""
        self.state = 'done'
        val = self.env['hospital.operation'].search([('id', '=', self.op_theater_id.id)])
        for rec in val:
            rec.write({
                'state': 'free'
            })

    def cancel_surgery(self):
        self.state = 'cancel'

    def _compute_age(self):
        """Age calculation of patient"""
        for rec in self:
            rec.patient_age = False
            if rec.dob:
                rec.patient_age = (date.today() - rec.dob) // timedelta(days=365.2425)

    @api.model
    def create(self, vals):
        if vals.get('surgery_seq', 'New') == 'New':
            vals['surgery_seq'] = self.env['ir.sequence'].next_by_code(
                'surgery.sequence') or 'New'
        result = super(HospitalSurgery, self).create(vals)
        return result


class HospitalInsurance(models.Model):
    _name = 'hospital.insurance'

    name = fields.Char()


class SurgeryType(models.Model):
    _name = 'surgery.type'

    name = fields.Char()


class Surgery(models.Model):
    _name = 'surgery.surgery'

    name = fields.Char()
    sur_cat = fields.Many2one('surgery.type', required='True', string='Surgery Category')
    sur_amount = fields.Float('Amount', compute='compute_surgery_total')
    estimate_hour = fields.Float('Estimate Hour')
    surgery_equipment_id = fields.One2many('surgery.line', 'product_surgery_id', 'Surgery Needs')

    @api.onchange('surgery_equipment_id.standard_price')
    def compute_surgery_total(self):
        for record in self:
            if record.surgery_equipment_id:
                for rec in record.surgery_equipment_id:
                    record.sur_amount += rec.standard_price
            else:
                record.sur_amount = 0


class SurgicalProduct(models.Model):
    _name = 'surgery.line'

    product_surgery_id = fields.Many2one('surgery.surgery')
    name_id = fields.Many2one('product.product','Name')
    standard_price = fields.Float('Price', related='name_id.list_price')


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def followup_patients(self):
        """Followups for patients about their surgery"""
        nxt_date = self.env['hospital.surgery'].search([])
        for rec in nxt_date:
            if rec.next_appointment and rec.next_appointment >= Date.today():
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                Urls = urls.url_join(base_url, '/appointment')
                mail_content = _('Hi %s,<br>'
                                 'Your Next Appointment for %s is arrived'
                                 '<div style = "text-align: left; margin-top: 16px;"><a href = "%s"'
                                 'style = "padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; '
                                 'border-color:#875A7B;text-decoration: none; display: inline-block; '
                                 'margin-bottom: 0px; font-weight: 400;text-align: center; vertical-align: middle; '
                                 'cursor: pointer; white-space: nowrap; background-image: none; '
                                 'background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px;">'
                                 'View %s</a></div>'
                                 ) % \
                               (rec.patient_name, rec.surgery_seq, Urls, rec.patient_name)
                email_to = self.env['res.partner'].search([('name', '=', rec.patient_name)])
                for mail in email_to:
                    main_content = {
                        'subject': _('Your Next Consultation(%s) Remainder') % rec.surgery_seq,
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': mail.email
                    }
                    mail_id = self.env['mail.mail'].create(main_content)
                    mail_id.mail_message_id.body = mail_content
                    mail_id.send()
