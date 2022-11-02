# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields


class ProductTags(models.Model):
    _name = 'product.tags'
    _description = 'Product Tags'

    name = fields.Char(string="Tag Name", required="1")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: