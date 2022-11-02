# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    direct_login = fields.Boolean(string="Direct Login")
    pos_config_id = fields.Many2one('pos.config', string="Session")
