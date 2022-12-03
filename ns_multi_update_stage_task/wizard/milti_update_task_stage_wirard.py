# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MultiUpdateTaskStage(models.TransientModel):
    _name = 'multi_update.task_stage'

    name = fields.Many2one('project.project', string=_("Project"))
    stage_id = fields.Many2one('project.task.type', string=_("Destination stage"))
    task_ids = fields.Many2many('project.task', 'multi_update_task_stage_task_rel', 'multi_update_id', 'task_id', string=_("Tasks linked"))
    check_domain = fields.Boolean(string=_("Check domain"), compute="_set_stage_and_task_domain")

    def ns_multi_update_stage_task_wizard_action(self):
        for line in self:
            list(map(lambda tasks: tasks.update({'stage_id': line.stage_id.id}), line.task_ids))

    @api.onchange('name')
    def _set_stage_and_task_domain(self):
        for line in self:
            line.check_domain = False
            domain = {}
            stage_ref = self.env['project.task.type'].search([]).filtered(lambda x: line.name.id in x.project_ids.mapped('id'))
            domain['stage_id'] = [('id', 'in', stage_ref.mapped('id'))]
            domain['task_ids'] = [('id', 'in', line.name.mapped('task_ids.id'))]
            return {'domain': domain}
