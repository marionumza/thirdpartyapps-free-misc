# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import models, api, _


class ir_model(models.Model):
    _inherit = "ir.model"

    def action_show_records(self):
        for model in self:
            return {
                "display_name": model.name,
                "name": model.name,
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "tree,form",
                "res_model": model.model,
                "views": [],
                "view_id": [],
                "target": "current",
                "context": self._context,
            }
