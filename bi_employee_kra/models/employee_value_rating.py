# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api,_
from odoo.exceptions import UserError


class emplotee_value(models.Model):
    _name = 'employee.value'
    _rec_name = "employee_id"


    @api.depends('system_proccess','follow_instructions','adaptable_flexible','ability_to_plan',
                'job_knowledge','skill_handke_work','learn_new_skill','accuracy','reliability','client_satisfaction',
                'work_on_time','work_under_pressure','handling_new_portfolio','relationship_co_workers',
                'problem_solving','decision_making','time_management','oral_written_expression',
                'sharing_of_knowledge','seek_t_d','open_to_ideas','enthusiastic','trustworthy',
                'work_place_ettiquttes','punctuality','discipline','attendance','team_work',
                'team_building','new_strategy_and_direction','participation_hr_activity')
    def _compute_total_avg (self):
        total = 0
        for line in self :

            total = (line.system_proccess + line.follow_instructions +line.adaptable_flexible +line.ability_to_plan +
                line.job_knowledge + line.skill_handke_work +line.learn_new_skill + line.accuracy + line.reliability +line.client_satisfaction +
                line.work_on_time +line.work_under_pressure +line.handling_new_portfolio +line.relationship_co_workers +
                line.problem_solving +line.decision_making+line.time_management +line.oral_written_expression +
                line.sharing_of_knowledge + line.seek_t_d + line.open_to_ideas +line.enthusiastic +line.trustworthy +

                line.work_place_ettiquttes + line.punctuality + line.discipline +line.attendance +line.team_work +
                line.team_building +line.new_strategy_and_direction + line.participation_hr_activity)

            
            avg = total/31

            line.total_avg = avg


        return


    # def _compute_leadership_score(self):
    #     return

    employee_id = fields.Many2one('hr.employee',string="Employee")
    job_id = fields.Many2one('hr.job',string="Job Position",related="employee_id.job_id")
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
                                
                             ],default="1",string="KRA Month",required=True)

    state = fields.Selection([('draft','Draft'),('cancel','Cancel'),('done','Done')],string='State',default="draft")
    employee_code  = fields.Integer(string="Employee Code",related="employee_id.id")

    appraiser_id = fields.Many2one('hr.employee',string="Appraiser",related="employee_id.parent_id")
    year_id = fields.Many2one('year.list',string="Year",required=True)

    total_avg = fields.Float(string="Total Average",compute="_compute_total_avg")
    leadership_score = fields.Float(string="Leadership Score")

    system_proccess = fields.Float(string="System And Proccesses")
    follow_instructions =  fields.Float(string="Follow Instructions")
    adaptable_flexible = fields.Float(string="Adaptable And Flexible")
    ability_to_plan = fields.Float(string="Ability To Plan")

    job_knowledge = fields.Float(string="Job Knowledge")
    skill_handke_work = fields.Float(string="Skill To Handle Work")
    learn_new_skill = fields.Float(string="Learn New Skill")


    accuracy = fields.Float(string="Accuracy")
    reliability = fields.Float(string="Reliability")
    client_satisfaction =  fields.Float(string="Client Satisfaction")


    work_on_time = fields.Float(string="Work Completion On Time")
    work_under_pressure = fields.Float(string="Ability To Work Under Pressure")
    handling_new_portfolio = fields.Float(string="Handling New Portfolio")


    relationship_co_workers = fields.Float(string="Relationship With Co-workers")
    problem_solving= fields.Float(string="Problem Solving")
    decision_making= fields.Float(string="Decision Making")
    time_management = fields.Float(string="Time Management")



    oral_written_expression = fields.Float(string="Oral And Written Expression")
    sharing_of_knowledge = fields.Float(string="Sharing Of Knowledge")


    seek_t_d = fields.Float(string="Seeks T & D")
    open_to_ideas = fields.Float(string="Open To Ideas")


    enthusiastic = fields.Float(string="Enthusiastic")
    trustworthy = fields.Float(string="Trustworthy")


    work_place_ettiquttes = fields.Float(string="Work Place Ettiquttes")
    punctuality = fields.Float(string="Punctuality")
    discipline = fields.Float(string="Discipline")
    attendance = fields.Float(string="Attendance")


    team_work = fields.Float(string="Team Work")
    team_building = fields.Float(string="Team Building")
    new_strategy_and_direction = fields.Float(string="New Strategy And Direction")
    participation_hr_activity = fields.Float(string="Participation In HR Activities")

    def cancel_kra (self):
        self.write({'state': 'cancel'})

        return 

    def done_kra (self):
        self.write({'state': 'done'})

        return




