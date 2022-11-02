from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    similarity_threshold = fields.Float(string='Similarity Threshold', config_parameter="similar_products.similarity_threshold", default=0.3)
