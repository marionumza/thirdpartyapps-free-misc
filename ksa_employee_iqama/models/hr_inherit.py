# -*- coding: utf-8 -*-
# Part of Musa Abdullah Abdalawahed. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import datetime

class HrKsaIqamaInherit(models.Model):
	_inherit = 'hr.employee'

	iqama_no = fields.Char(string="Iqama Number", tracking=True)
	iqama_position = fields.Char(string="Iqama Job", tracking=True)
	place_of_issue = fields.Char(string="Place of Issue", tracking=True)
	date_of_issue = fields.Date(string="Date of Issue", tracking=True)
	date_of_expiry = fields.Date(string="Date of Expiry", tracking=True)
	# iqama_state = fields.Selection([('valid','Valid'), ('not_valid','Not Valid')], string="Iqama state", default="valid")
	religion = fields.Char(string="Religion", tracking=True)
	# is_iqama_valid = fields.Boolean(string="Is valid", compute="_compute_valid_iqama")
	# iqama_count = fields.Char(string="Iquam Expire", compute="_compute_visa_count")
	current_date = fields.Date(string="Current date", default=datetime.date.today())


    # def _compute_valid_iqama(self):



	# @api.depends("birthday")
	# def _compute_age(self):
	# 		for rec in self:
	# 			rec.employee_age = relativedelta(datetime.date.today(),rec.birthday).years;
	#
	# def _compute_passport_count(self):
	# 	for rec in self:
	# 		if rec.passport_expire:
	# 			rec.passport_count = abs((rec.passport_expire - rec.current_date).days)
	# 		else:
	# 			rec.passport_count = 0
	#
	# @api.depends("visa_expire")
	# def _compute_visa_count(self):
	# 	for rec in self:
	# 		if rec.visa_expire:
	# 			rec.iquam_count = abs((rec.visa_expire - rec.current_date).days)
	# 		else:
	# 			rec.iquam_count = 0