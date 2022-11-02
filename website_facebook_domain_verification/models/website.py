# -*- coding: utf-8 -*-

from odoo import fields, models



class Website(models.Model):
    _inherit = "website"

    facebook_domain_verification_code = fields.Char(
        string='Verification Code',
        help='Facebook Domain Verification Code',
    )
