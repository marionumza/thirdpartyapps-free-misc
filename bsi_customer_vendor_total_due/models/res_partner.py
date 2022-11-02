# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt ltd'<www.botspotinfoware.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"

    bsi_total_due = fields.Float(compute="compute_total_due", string="Amount Due")
    bsi_credit_due = fields.Float(compute="_compute_total_credit_due", string="Credit Due")

    # This compute method used for finding total amount due...
    def compute_total_due(self):
        for record in self:
            total_amount_due = 0.0
            amount_dues = self.env['account.move'].search([('partner_id', '=', record.id), ('move_type', '=', 'out_invoice')])
            for amount_due in amount_dues:
                total_amount_due += amount_due.amount_residual
            record.bsi_total_due = total_amount_due
            amount_dues = self.env['account.move'].search([('partner_id', '=', record.id), ('move_type', '=', 'in_invoice')])
            for amount_due in amount_dues:
                total_amount_due += amount_due.amount_residual
            record.bsi_total_due = total_amount_due


    # This compute method used for finding total credit note due...
    def _compute_total_credit_due(self):
        for record in self:
            total_amount_due = 0
            amount_dues = self.env['account.move'].search([('partner_id', '=', record.id), ('move_type', '=', 'out_refund')])
            for amount_due in amount_dues:
                total_amount_due += amount_due.amount_residual
            record.bsi_credit_due = total_amount_due
            amount_dues = self.env['account.move'].search([('partner_id', '=', record.id), ('move_type', '=', 'in_refund')])
            for amount_due in amount_dues:
                total_amount_due += amount_due.amount_residual
            record.bsi_credit_due = total_amount_due
