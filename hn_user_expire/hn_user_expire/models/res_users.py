# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date

import logging
_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    expiration_date = fields.Date(string='Expiration date', copy=True)

    @api.model
    def check_expired_access(self, *args, **kwargs):
        users = self.search([])
        for user in users:
            if user.expiration_date and user.expiration_date < date.today():
                user.active = False
