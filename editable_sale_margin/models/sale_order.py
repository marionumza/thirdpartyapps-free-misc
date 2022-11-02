# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin = fields.Float("Margin", digits='Product Price', readonly=False, store=True, groups="base.group_user")
    margin_percent = fields.Float("Margin (%)", store=True, readonly=False, groups="base.group_user")

    @api.onchange('price_subtotal', 'margin_percent')
    def onchange_margin_percent(self):
        self.margin = self.price_subtotal - (self.purchase_price * self.product_uom_qty)
        if self._context.get('margin_percent'):
            self.margin_percent = self._context.get('margin_percent')
        if self.purchase_price > 0.0 and self.margin_percent and not self._context.get('get_sizes'):
            margin_percent = self.margin_percent
            montant_extras = self.purchase_price * (self.margin_percent)
            self.price_unit = self.purchase_price + montant_extras
            self.margin_percent = margin_percent
            context = dict(self.env.context)
            context.update({'get_sizes': True, 'margin_percent': margin_percent})
            self.env.context = context

    @api.onchange('product_uom_qty', 'purchase_price', 'discount')
    def compute_margin_1(self):
        self.margin = self.price_subtotal - (self.purchase_price * self.product_uom_qty)
        self.margin_percent = self.purchase_price and self.margin / self.purchase_price
        context = dict(self.env.context)
        context.update({'get_sizes': True})
        self.env.context = context

    @api.onchange('price_unit')
    def onchange_price_unit_1(self):
        if self.price_unit and not self._context.get('get_sizes'):
            self.write({'margin_percent': self.purchase_price and self.margin / self.purchase_price})
            context = dict(self.env.context)
            context.update({'get_sizes': True})
            self.env.context = context

    @api.onchange('margin')
    def onchange_margin(self):
        if self.price_unit and not self._context.get('get_sizes') and not self._context.get('margin_percent'):
            self.price_unit = self.purchase_price + self.margin

