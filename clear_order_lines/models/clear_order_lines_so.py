from odoo import models


class ClearSalesOrder(models.Model):
    _inherit = "sale.order"

    def show_popup(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'clear.order.lines.so',
            'view_mode': 'form',
            'target': 'new',
        }
