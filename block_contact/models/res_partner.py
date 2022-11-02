from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_block_user = fields.Selection([('False', 'Not Blocked'),('True', 'Blocked')], default = "False", string = 'Block User: ')
