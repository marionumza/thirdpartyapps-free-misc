# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_round
from odoo import SUPERUSER_ID
import datetime as dt


class product_product(models.Model):
    _inherit = 'product.product'


    suggested_product_id=fields.Many2many('product.product', 'product_rel_product', 'origin_id', 'similar_id' , string='Suggested Products')
   

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: