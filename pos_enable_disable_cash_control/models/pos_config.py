# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _


class PosConfig(models.Model):
    _inherit = 'pos.config'
    is_cash_control_enable_disable = fields.Boolean(string='Enable / Disable Cash Control', default=False)

    @api.depends('payment_method_ids')
    def _compute_cash_control(self):
        res = super(PosConfig, self)._compute_cash_control()
        for rec in self:
            if rec.is_cash_control_enable_disable == False:
                rec.cash_control = False
            else:
                rec.cash_control = True
        return res
