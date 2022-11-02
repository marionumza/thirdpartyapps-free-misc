# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

# Standard library imports
import logging

# Odoo imports
from odoo import models, fields, api

log = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = 'project.task'

    customer_asset_id = fields.Many2one('customer.asset', string='Customer Asset')
