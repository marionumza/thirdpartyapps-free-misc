# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

today = date.today()

class deeu(models.Model):
    _name = 'deeu'

    def deactivate_expired_employee_user(self):
        today = date.today()
        emps = self.env['hr.employee'].search_read([],['id','user_id'])
        for emp in emps:
            valid_contracts = self.env['hr.contract'].search_read([('employee_id','=',emp['id']),('date_end','>', today )],['id'], offset=0, limit=1, order="date_end desc")
            if len(valid_contracts) > 0:
                print('Nothing to do here!')
            else:
                users = self.env['res.users'].search([('id', '=',emp['user_id'][0])])
                for user in users:
                    user.write({'active': False})
