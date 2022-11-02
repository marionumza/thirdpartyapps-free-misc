# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OdooServerActionResultWizard(models.TransientModel):
    _name = 'odoo.server.action.result.wizard'
    _description = 'Server Action Result Wizard'

    body = fields.Text()
