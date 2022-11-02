from odoo import models, fields, api, _


class FreeOfCostReason(models.Model):
    _name = 'foc.reason'
    _description = 'Free of Cost Reason '

    name = fields.Char(string='Reason')



