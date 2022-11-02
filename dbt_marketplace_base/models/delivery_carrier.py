#/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CustomDeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    transporter_ids = fields.Many2many(
        string='Transporters',
        comodel_name='dbt.transporter',
        relation='carrier_transporter_rel',
        column1='carrier_id',
        column2='transporter_id',
    )