from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def mark_customer(self):
        for rec in self:
            rec.customer_rank = 1


    def mark_supplier(self):
        for rec in self:
            rec.supplier_rank = 1


