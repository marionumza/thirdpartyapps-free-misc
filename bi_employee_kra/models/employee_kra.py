# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api,_
from odoo.exceptions import UserError


class KRA(models.Model):
    _name = 'employee.kra'
    _rec_name = "employee_id"


    month = fields.Selection([
                                ('1','January'),
                                ('2','February'),
                                ('3','March'),
                                ('4','April'),
                                ('5','May'),
                                ('6','June'),
                                ('7','July'),
                                ('8','August'),
                                ('9','September'),
                                ('10','October'),
                                ('11','November'),
                                ('12','December')
                                
                             ],default="1",string="KRA Month")

    

    state = fields.Selection([('draft','Draft'),('submit','Submit To Supervisor'),('cancel','Cancel'),('done','Done')],string='State',default="draft")

    kra_quarter = fields.Selection([('1','First Quarter'),('2','Second Quarter'),('3','Third Quarter'),('4','Fourth Quarter')],string="Quarter")

    year_id = fields.Many2one('year.list',string="Year")

    kra_id = fields.Many2one('hr.kra',string="KRA")

    questions_ids = fields.One2many('kra.questions','employee_kra_id',string="Questions")

    employee_id = fields.Many2one('hr.employee',string="Employee")

    total_employee_rating = fields.Float(string="Total Employee Rating",compute="_compute_rating",store=True)
    total_manager_rating  = fields.Float(string="Total Manager Rating",compute="_compute_rating",store=True)
    total_final_score = fields.Float(string="Total Final Score",compute="_compute_rating",store=True)


    @api.depends('questions_ids')
    def _compute_rating(self):

        for line in self :
            total_emp = 0
            total_manger = 0
            total_final = 0 
            for rate in line.questions_ids:

                total_emp = total_emp + rate.employee_rating
                total_manger = total_manger + rate.manager_rating
                total_final = total_final + rate.final_score

            line.total_employee_rating = total_emp
            line.total_manager_rating = total_manger
            line.total_final_score = total_final



        return



    def submit_to_supervisor(self):

        self.write({'state': 'submit'})

        return 


    def cancel_kra (self):
        self.write({'state': 'cancel'})

        return 


    def done_kra (self):
        self.write({'state': 'done'})

        return 


class Year_list(models.Model):
    _name = 'year.list'


    name = fields.Char(string="Year")

    



