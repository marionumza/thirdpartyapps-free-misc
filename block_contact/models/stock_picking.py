from odoo import api, models, fields, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_current_block_status = fields.Selection([],readonly = True, store = True, copied = True, related = "partner_id.x_block_user", string = "Blocking Status")