# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class POSConfigInherit(models.Model):
    _inherit = 'pos.config'
    _description = 'Backend POS'

    def open_session_cb_backend(self, check_coa=True):
        """ new session button

        create one if none exist
        access cash control interface if enabled or start a session
        """
        self.ensure_one()
        if not self.current_session_id:
            self._check_company_journal()
            self._check_company_invoice_journal()
            self._check_company_payment()
            self._check_currencies()
            self._check_profit_loss_cash_journal()
            self._check_payment_method_ids()
            self._check_payment_method_receivable_accounts()
            self.env['pos.session'].create({
                'user_id': self.env.uid,
                'config_id': self.id
            })
        return self.open_ui_backend()

    def open_ui_backend(self):
        """Open the pos interface with config_id as an extra argument.

        In vanilla PoS each user can only have one active session, therefore it was not needed to pass the config_id
        on opening a session. It is also possible to login to sessions created by other users.

        :returns: dict
        """
        self.ensure_one()
        # check all constraints, raises if any is not met
        self._validate_fields(set(self._fields) - {"cash_control"})
        session_id = self.env['pos.session'].search([('config_id', '=', self.id), ('state', '=', 'opened')]).id
        return {
            'name': _('Session Opened'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'pos.session',
            'view_id': self.env.ref('backend_pos_by_fas.pos_session_form_view_backend').id,
            'target': 'current',
            'res_id': session_id,
            'context': {'edit': False},
        }

    def open_existing_session_cb_backend(self):
        """ close session button

        access session form to validate entries
        """
        self.ensure_one()
        return self._open_session_backend(self.current_session_id.id)

    def _open_session_backend(self, session_id):
        return {
            'name': _('Session'),
            'view_mode': 'form',
            'res_model': 'pos.session',
            'res_id': session_id,
            'view_id': self.env.ref('backend_pos_by_fas.pos_session_form_view_backend').id,
            'type': 'ir.actions.act_window',
        }