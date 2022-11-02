# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools

class employee_kra_report(models.Model):
    _name = "employee.kra.report"
    _description = "Employee Value"
    _auto = False


    employee_id = fields.Many2one('hr.employee',string="Employee")
    employee_rating = fields.Float('Employee Rating')
    manager_rating = fields.Float('Manager Rating')
    final_score = fields.Float('Final Score')
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'employee_kra_report')
        self._cr.execute("""
            CREATE or REPLACE VIEW employee_kra_report as (
                SELECT
                    min(kra.id) as id,
                    kra.employee_id as employee_id, 
                    
                    kra.total_employee_rating as employee_rating,
                    kra.total_manager_rating as manager_rating,
                    kra.total_final_score as final_score
                    
                FROM
                    employee_kra as kra
             
                GROUP BY
                    employee_id,
                    employee_rating,
                    manager_rating,
                    final_score
     
        )""" 
        )





