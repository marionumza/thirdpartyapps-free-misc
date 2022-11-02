# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'


    trainer = fields.Boolean(string='Is Trainer', )
    trainer_type = fields.Selection(selection=[('personal', 'Personal'), ('general', 'General'),
                                               ], default='general', )
