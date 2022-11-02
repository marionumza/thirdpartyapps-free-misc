# Copyright 2020-22 Manish Kumar Bohra <manishkumarbohra@outlook.com>
# License LGPL-3 - See http://www.gnu.org/licenses/Lgpl-3.0.html

from odoo import api, fields, models
from datetime import date


class CancelQuotationExpired(models.Model):
    _inherit = 'sale.order'

    def cancel_qut_expired(self):
        """This method mainly use for the cron action to cancel the expired quotations"""
        for records in self.env['sale.order'].search(
                [('state', 'in', ['draft', 'sent']), ('validity_date', '<', date.today())]):
            records.update({'state': 'cancel'})
