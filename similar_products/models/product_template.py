from odoo import models, fields


class SimilarMixInProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'similar.products.mixin']

    similar_products = fields.One2many('similar.products', 'product_template_id', string='Similar Products', copy=True)
