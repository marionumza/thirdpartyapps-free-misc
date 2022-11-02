# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Kra_wizard(models.TransientModel):
	_name = "kra.wizard"


	month = fields.Selection([
					('1','January'),('2','February'),
					('3','March'),('4','April'),
					('5','May'),('6','June'),
					('7','July'),('8','August'),
					('9','September'),('10','October'),
					('11','November'),('12','December')
					],default="1",string="KRA Month",required=True)

	year_id = fields.Many2one('year.list',string="Year",required=True)
	kra_quarter = fields.Selection([('1','First Quarter'),('2','Second Quarter'),('3','Third Quarter'),('4','Fourth Quarter')],string="Quarter")
	employee_ids = fields.Many2many('hr.employee','rel_kra_employee_wizard',string="Employee")
	all_employee = fields.Boolean(string = 'All Employee')


	def create_kra (self):
		employee_rec = self.env['hr.employee'].search([])
		kra_employee_obj = self.env['employee.kra']
		questions_obj = self.env['kra.questions']

		if self.all_employee == True :
			for emp in employee_rec :
				if emp.job_id.kra_id :

					kra_emp = kra_employee_obj.create({
						'month' : self.month,
						'kra_quarter' : self.kra_quarter,
						'year_id' : self.year_id.id,
						'kra_id':emp.job_id.kra_id.id,
						'employee_id' : emp.id,
						})

					for ques in emp.job_id.kra_id.questions_ids:
						questions_obj.create({
							'name': ques.name,
							'description': ques.description,
							'hint':ques.hint,
							'weightage':ques.weightage,
							'employee_kra_id' : kra_emp.id
							})

		else :
			for emp in self.employee_ids :
				
				if emp.job_id.kra_id :
					kra_emp = kra_employee_obj.create({
						'month' : self.month,
						'kra_quarter' : self.kra_quarter,
						'year_id' : self.year_id.id,
						'kra_id':emp.job_id.kra_id.id,
						'employee_id' : emp.id,
						})

					for ques in emp.job_id.kra_id.questions_ids:
						questions_obj.create({
							'name': ques.name,
							'description': ques.description,
							'hint':ques.hint,
							'weightage':ques.weightage,
							'employee_kra_id' : kra_emp.id
							})
				else:
					raise UserError(_("Please set KRA for '%s' job position !") % emp.job_id.name)
		return

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: