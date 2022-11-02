from odoo import api, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_account_payable_recievable(self):
        account_id = self.journal_id.account_currency_ids.filtered(lambda l: l.currency_id == self.currency_id).account_id
        if account_id:
            return account_id
        elif self.partner_id:
            # Retrieve account from partner.
            if self.is_sale_document(include_receipts=True):
                return self.partner_id.property_account_receivable_id
            else:
                return self.partner_id.property_account_payable_id
        else:
            # Search new account.
            domain = [
                ('company_id', '=', self.company_id.id),
                ('internal_type', '=', 'receivable' if self.move_type in ('out_invoice', 'out_refund', 'out_receipt') else 'payable'),
            ]
            return self.env['account.account'].search(domain, limit=1)

    def _change_payable_receivable_account(self):
        account_id = self._get_account_payable_recievable()
        for line in self.line_ids.filtered(lambda l: l.account_id.user_type_id.type in ('receivable', 'payable')):
            line.account_id = account_id
            
    @api.onchange('journal_id')
    def _onchange_journal(self):
        res = super(AccountMove, self)._onchange_journal()
        self._change_payable_receivable_account()
        return res

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self._change_payable_receivable_account()
        return res

    @api.onchange('date', 'currency_id')
    def _onchange_currency(self):
        res = super(AccountMove, self)._onchange_currency()
        self._change_payable_receivable_account()
        return res

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        res = super(AccountMove, self)._onchange_invoice_line_ids()
        self._change_payable_receivable_account()
        return res
