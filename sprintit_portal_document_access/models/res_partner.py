# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<https://sprintit.fi>).
#
##############################################################################

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    portal_document_access = fields.Boolean('Portal Documents Access', default=False, copy=False)
    