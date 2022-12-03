# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import models, fields, api, _


class InheritProjectTask(models.Model):
    _inherit = 'project.task'

    def ns_multi_update_stage_task_action(self):
        all_project_ref = self.mapped('project_id')
        check_update_not_same_stage_task = self.env['ir.config_parameter'].sudo().get_param(
            'ns_multi_update_stage_task.group_accept_not_same_stage', False)
        if len(all_project_ref.mapped('id')) != 1:
            raise UserError(_(
                "You can't Proceed to multi-update of stage of task becauce the tasks is not have the same projet (Only the tasks in same projet can use this fonctionality)"))
        if len(list(set(self.mapped('stage_id.id')))) > 1 and check_update_not_same_stage_task is False:
            raise UserError(
                _("You can't Proceed to multi-update of stage of task because all task is not in the same stage!"))

        return {
            'name': _('Multi-update of stage of task'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi_update.task_stage',
            'target': 'new',
            'context': {
                'default_name': all_project_ref.mapped('id')[0],
                'default_task_ids': [(6, 0, self.mapped('id'))],
            },
        }
