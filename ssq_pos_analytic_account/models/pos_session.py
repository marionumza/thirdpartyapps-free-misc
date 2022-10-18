from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_sale_vals(self, key, amount, amount_converted):
        account_id, sign, tax_keys, base_tag_ids = key
        tax_ids = {tax[0] for tax in tax_keys}
        applied_taxes = self.env["account.tax"].browse(tax_ids)
        title = "Sales" if sign == 1 else "Refund"
        name = "%s untaxed" % title
        if applied_taxes:
            name = "{} with {}".format(title, ", ".join([tax.name for tax in applied_taxes]))
        partial_vals = {
            "name": name,
            "account_id": account_id,
            "analytic_account_id": self.config_id.analytic_account_id.id
            if self.config_id.analytic_account_id
            else False,
            "move_id": self.move_id.id,
            "tax_ids": [(6, 0, tax_ids)],
            "tax_tag_ids": [(6, 0, base_tag_ids)],
        }
        return self._credit_amounts(partial_vals, amount, amount_converted)
