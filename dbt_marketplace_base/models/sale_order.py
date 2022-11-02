
#/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

    transporter_id = fields.Many2one(
        string='Transporter',
        comodel_name='dbt.transporter',
        ondelete='restrict',
    )
    sale_order_source = fields.Many2one('sale.order.source','Source Of Order')    