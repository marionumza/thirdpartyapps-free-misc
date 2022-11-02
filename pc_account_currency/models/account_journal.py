from odoo import fields, models

class AccountJounal(models.Model):
    _inherit = 'account.journal'

    account_currency_ids = fields.One2many(comodel_name='account.currency', inverse_name='journal_id', string='Account by currency')
