# -*- coding: utf-8 -*-
# Part of SysNeo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    planned_revenue_second = fields.Monetary('Revenue Other Currency', currency_field='currency_id', tracking=True)

    @api.onchange('currency_id','planned_revenue_second')
    def _onchange_planned_revenue(self):
        if self.currency_id:
            self.planned_revenue = self.currency_id._convert(self.planned_revenue_second, self.company_currency, self.company_id, self.create_date)