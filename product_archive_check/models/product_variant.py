# -*- coding: utf-8 -*-
# Copyright 2020-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import models
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    def write(self,vals):
        for rec in self:
            if 'active' in vals and not vals.get('active') and rec.qty_available != 0.0:
                raise UserError("You can not archive the product as the onhand quantity is still there.")
        return super(ProductProduct, self).write(vals)
