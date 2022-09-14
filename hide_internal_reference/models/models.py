# -*- coding: utf-8 -*-

from odoo import api, fields, models


class product_product(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        def _name_get(d):
            return (d['id'], d['name'])

        result = []
        for product in self.sudo():
            mydict = {
                'id': product.id,
                'name': product.name,
            }
            result.append(_name_get(mydict))
        return result
