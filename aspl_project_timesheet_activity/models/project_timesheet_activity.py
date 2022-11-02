import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProjectTimesheetActivity(models.Model):
    _name = "project.timesheet.activity"
    _description = "Project Timesheet Activity"

    name = fields.Char("Activity")



class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    timesheet_activity_id = fields.Many2one('project.timesheet.activity',"Activity")
