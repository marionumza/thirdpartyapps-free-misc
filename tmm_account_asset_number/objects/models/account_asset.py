# -*- coding: utf-8 -*-
# Copyright 2021 Gusti Tammam

from odoo import api, fields, models


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    _sql_constraints = [('number_unique', 'UNIQUE (number)', 'Asset Number should be unique!')]

    number = fields.Char(string="Asset Number", required=False, copy=False)

    def validate(self):
        super(AccountAsset, self).validate()
        sequence_obj_sudo = self.env['ir.sequence'].sudo()
        for asset in self:
            if not asset.number:
                asset.write({'number': sequence_obj_sudo.next_by_code('account.asset.sequence')})
