from odoo import models


class ClearPurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def show_popup_po(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'clear.order.lines.po',
            'view_mode': 'form',
            'target': 'new',
        }
