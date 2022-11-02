# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class POSOrderInherit(models.Model):
    _inherit = 'pos.order'
    _description = 'Backend POS Order'

    amount_tax = fields.Float(string='Taxes', digits=0, readonly=True, required=False)
    amount_total = fields.Float(string='Total', digits=0, readonly=True, required=False)
    amount_paid = fields.Float(string='Paid', states={'draft': [('readonly', False)]},
                               readonly=True, digits=0, required=False)
    amount_return = fields.Float(string='Returned', digits=0, required=False, readonly=True)