#/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SalesOrderSource(models.Model):
    _name = 'sale.order.source'
    _description = "Sale Order Source"

    name = fields.Char('Name')
    code = fields.Char('Code')

    provides_label = fields.Boolean('Does this marketplace provide shipping labels')

    relevant_sales = fields.One2many('sale.order', 'sale_order_source', string='Sales Orders')
    # relevant_transporters = fields.Many2many('dbt.transporter', string='Transporters')

class ShipmentTransporter(models.Model):
    _name = "dbt.transporter"
    _description = "Shipment Transporter"

    name = fields.Char('Name')
    active = fields.Boolean('Active')    
    transporter_code = fields.Char('Transporter Code')
     
    carrier_ids = fields.Many2many(
        string='carrier',
        comodel_name='delivery.carrier',
        relation='carrier_transporter_rel',
        column1='transporter_id',
        column2='carrier_id',
    )

    # related_source_ids = fields.Many2many('sale.order.source', string='Source Of Transportation')

    _sql_constraints = [('transporter_code_uniq', 'unique (transporter_code)',
                     'Duplicate transporter code not allowed !')]