# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools

class employee_kra_report(models.Model):
    _name = "employee.value.report"
    _description = "Employee Value"
    _auto = False


    employee_id = fields.Many2one('hr.employee',string="Employee")

    sharing_of_knowledge = fields.Float('Sharing Of Knowledge')
    follow_instructions = fields.Float('Follow Instructions')
    enthusiastic = fields.Float('Enthusiastic')
    problem_solving = fields.Float('Problem Solving')
    client_satisfaction = fields.Float('Client Satisfaction')
    learn_new_skill = fields.Float('Learn New Skill')


    def init(self):
        tools.drop_view_if_exists(self._cr, 'employee_value_report')
        self._cr.execute("""
            CREATE or REPLACE VIEW employee_value_report as (
                SELECT
                    min(value.id) as id,
                    value.employee_id as employee_id, 
                    
                    value.sharing_of_knowledge as sharing_of_knowledge,
                    value.follow_instructions as follow_instructions,
                    value.enthusiastic as enthusiastic,

                    value.problem_solving as problem_solving,
                    value.client_satisfaction as client_satisfaction,
                    value.learn_new_skill as learn_new_skill
                    
                FROM
                    employee_value as value
                    
                GROUP BY
                    employee_id,
                    sharing_of_knowledge,
                    follow_instructions,
                    enthusiastic,
                    problem_solving,
                    client_satisfaction,
                    learn_new_skill
          
        )""" 
        )





