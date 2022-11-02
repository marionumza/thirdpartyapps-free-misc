from odoo import models, fields


class SimilarMixInProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'similar.products.mixin']

    similar_products = fields.One2many('similar.products', 'product_product_id', string='Similar Products', copy=True)
