from odoo import models, fields, api


class Division(models.Model):
    _name = 'category.category'

    name = fields.Char(required=True)
    subcategory_ids = fields.One2many("subcategory.subcategory", "category_id", readonly=True)
