# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api,_
from odoo.exceptions import UserError


class KRA(models.Model):
    _name = 'hr.kra'



    name = fields.Char(string="Name")
    questions_ids = fields.One2many('kra.questions','kra_id',string="Questions")
    



class Kra_Questions(models.Model):

    _name = 'kra.questions'


    name = fields.Char(string="Questions")
    description = fields.Char(string="Description")
    hint = fields.Char(string="Hint")
    weightage = fields.Integer(string="Weightage")

    employee_rating = fields.Float(string = "Employee Rating")
    employee_remark = fields.Char(string="Employee Remark")

    manager_rating = fields.Float(string = "Manager Rating")
    manager_remark = fields.Char(string="Manager Remark")
    final_score = fields.Float(string="Final Score")


    kra_id = fields.Many2one('hr.kra',string="Kra")

    employee_kra_id = fields.Many2one('employee.kra',string="Employee Kra")


    state = fields.Selection([('draft','Draft'),('submit','Submit To Supervisor'),('cancel','Cancel'),('done','Done')],string='State',default="draft",related="employee_kra_id.state")
