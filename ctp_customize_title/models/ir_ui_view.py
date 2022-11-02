# -*- coding: utf-8 -*-
from odoo import api, models, _

class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def _render_template(self, template, values=None, engine='ir.qweb'):
        if template in ['web.login', 'web.webclient_bootstrap']:
            if not values:
                values = {}
            values["title"] = self.env['ir.config_parameter'].sudo().get_param("ctp_title", "")
        return super(View, self)._render_template(template, values, engine)
