from odoo import fields, models

class AccountCurrency(models.Model):
    _name = 'account.currency'
    _description = 'Account by Currency Line'

    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    account_id = fields.Many2one(comodel_name='account.account', string='Account')

    