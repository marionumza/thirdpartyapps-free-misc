# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    facebook_category_id = fields.Many2one(
        comodel_name='product.facebook.category',
        string='Facebook Category',
    )
