# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api

class srMultiBarcode(models.Model):
    _name = 'sr.multi.barcode'
    
    name = fields.Char('Barcode', required=True)
    product_tmpl_id = fields.Many2one('product.template','Product')
    product_id = fields.Many2one('product.product','Product Variant')

    _sql_constraints = [
        ('multi_barcode_unique', 'unique (name)', 'Barcode Must be different !')
    ]

