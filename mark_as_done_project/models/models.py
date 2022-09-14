# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class education_history(models.Model):
    _inherit = 'project.project'

    status = fields.Boolean('Status',default=False)

    def action_view_timesheet(self):
        if not self.id or self.ids.__len__()>1:
            raise ValidationError('Project overview can not be open for multiple projects.')
        self.ensure_one()
        if self.allow_timesheets:
            return self.action_view_timesheet_plan()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Timesheets of %s') % self.name,
            'domain': [('project_id', '!=', False)],
            'res_model': 'account.analytic.line',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _("""
                <p class="o_view_nocontent_smiling_face">
                    Record timesheets
                </p><p>
                    You can register and track your workings hours by project every
                    day. Every time spent on a project will become a cost and can be re-invoiced to
                    customers if required.
                </p>
            """),
            'limit': 80,
            'context': {
                'default_project_id': self.id,
                'search_default_project_id': [self.id]
            }
        }

    def get_partner_id(self):
        return self.partner_id.id
    def mark_archive(self):
        if self.partner_id.check_domain==True:
            domain = [('partner_id','=',self.partner_id.id)]
        else:
            domain = []
        self.active = False
        return {
            'name': 'Projects',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': self.env.ref('project.view_project_kanban').id,
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': domain
        }
    def mark_active(self):
        self.active = True
        return {
            'name': 'Archived Projects',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': self.env.ref('project.view_project_kanban').id,
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': [('active','=',False)]
        }

    def mark_done(self):
        if self.partner_id.check_domain==True:
            domain = [('partner_id','=',self.partner_id.id)]
        else:
            domain = []
        self.status = True
        return {
            'name': 'Projects',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': self.env.ref('project.view_project_kanban').id,
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain':domain

        }

    def mark_uncomplete(self):
        if self.partner_id.check_domain==True:
            domain = [('partner_id','=',self.partner_id.id)]
        else:
            domain = []
        self.status = False
        return {
            'name': 'Projects',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': self.env.ref('project.view_project_kanban').id,
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': domain
        }


class ResPartner(models.Model):
    _inherit = 'res.partner'
    check_domain = fields.Boolean()
