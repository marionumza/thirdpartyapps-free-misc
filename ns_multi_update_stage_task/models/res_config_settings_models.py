# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InheritResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_accept_not_same_stage = fields.Boolean(_("Accept multi-update of stage of tasks that are not in the same stage"), implied_group="project.group_project_manager")

    def set_values(self):
        res = super(InheritResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('ns_multi_update_stage_task.group_accept_not_same_stage', self.group_accept_not_same_stage)
        return res

    @api.model
    def get_values(self):
        res = super(InheritResConfigSettings, self).get_values()
        group_accept_not_same_stage_res = self.env['ir.config_parameter'].get_param('ns_multi_update_stage_task.group_accept_not_same_stage')
        res.update(
            group_accept_not_same_stage=group_accept_not_same_stage_res,
        )
        return res
