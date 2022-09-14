from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_multi_product_selection_wizard(self):
        return self.env['sale.multi.products'].wizard_view()