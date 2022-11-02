from odoo import models, fields


class SimilarProducts(models.TransientModel):
    _name = "similar.products"
    _description = "Temporarily stores similar products"

    product_template_id = fields.Many2one('product.template', index=True, required=False, ondelete='cascade')
    product_product_id = fields.Many2one('product.product', index=True, required=False, ondelete='cascade')

    similar_id = fields.Many2one('product.template', required=False, ondelete='cascade')
    similar_code = fields.Char(comodel_name='product.template', related='similar_id.default_code')
    similar_name = fields.Char(comodel_name='product.template', related='similar_id.name')
