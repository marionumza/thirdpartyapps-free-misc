# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('invoice_date')
    def _onchange_control_invoice_date(self):
        if self.invoice_date and self.move_type in ['out_invoice', 'out_refund'] and self.invoice_date < fields.Date.today():
            raise UserError(_('The invoice date chosen is in the past. '
                            'You must choose a date greater than or equal to today'
                              )
                            )

    @api.constrains('invoice_date')
    def _check_invoice_date(self):
        for rec in self:
            if rec.invoice_date and self.move_type in ['out_invoice', 'out_refund'] and rec.invoice_date < fields.Date.today():
                raise ValidationError(_('The invoice date chosen is in the past. '
                                        'You must choose a date greater than or equal to today'
                                        )
                                      )
