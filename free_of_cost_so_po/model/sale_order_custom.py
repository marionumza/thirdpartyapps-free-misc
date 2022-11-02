from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    foc_reason_id = fields.Many2one('foc.reason', store=True, string='Reason')
    foc = fields.Boolean('Non Billable', default=0)

    @api.onchange('foc')
    def _free_of_cost(self):
        for rec in self:
            if rec.foc == True:
                rec.price_unit = 0
