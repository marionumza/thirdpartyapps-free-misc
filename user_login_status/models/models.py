# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import timedelta


class UserLoginStatus(models.Model):
    _inherit = 'res.users'

    status = fields.Selection(selection=[
        ('done', 'Online'),
        ('blocked', 'Offline'),
    ], string="Login Status", default='blocked', readonly=1)

    total_log_record = fields.Integer('Total Log Information',compute='_count_total_log')

    def _count_total_log(self):
        for record in self:
            record.total_log_record = self.env['res.users.logger'].sudo().search([('username','=',record.id)],count=True)

    def show_log_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.users.logger",
            "domain": [('username','=',self.id)],
            "name": "User Logging Record",
            'view_mode': 'list',
        }

class UserLog(models.Model):
    _name = 'res.users.logger'

    username = fields.Many2one('res.users',"User Name")
    login_time = fields.Datetime("Login Time")
    logout_time = fields.Datetime("Logout Time")
    system_use_time = fields.Char("System Use Time",compute='_compute_system_use_time')


    def _compute_system_use_time(self):
        for record in self:
            if record.logout_time:
                time_diff = str(record.logout_time - record.login_time)
            else:
                time_diff = str(fields.Datetime.now() - record.login_time)
            time_diff = time_diff[:time_diff.find('.')]
            record.system_use_time = time_diff
