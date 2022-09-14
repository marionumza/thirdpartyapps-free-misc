from odoo import api, fields, models, osv


class PreventCreateNewProductOnSalesOrderLines(osv.osv.Model):
    _inherit = 'sale.order'


class PreventCreateNewProductOnPurchaseOrderLines(osv.osv.Model):
    _inherit = 'purchase.order'
