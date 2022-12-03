from odoo import models, fields, api


class Subdivision(models.Model):
    _name = 'subcategory.subcategory'

    name = fields.Char(required=True)
    category_id = fields.Many2one('category.category', 'Category', required=True)
