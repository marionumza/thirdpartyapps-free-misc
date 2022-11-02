# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class ResConfigInherit(models.TransientModel):
	_inherit = 'res.config.settings'

	draft_id = fields.Many2one('res.users', string = 'Draft')
	sent_id = fields.Many2one('res.users', string = 'Sent')
	purchase_order_id = fields.Many2one('res.users', string = 'Purchase Order')
	purchase_user_assign = fields.Boolean(string="User/Salesperson Assignment")

	@api.model
	def get_values(self):
		res = super(ResConfigInherit, self).get_values()
		pur_Sudo = self.env['ir.config_parameter'].sudo()
		draft_id = pur_Sudo.get_param('bi_assign_users_for_purchase.draft_id')
		sent_id = pur_Sudo.get_param('bi_assign_users_for_purchase.sent_id')
		purchase_order_id = pur_Sudo.get_param('bi_assign_users_for_purchase.purchase_order_id')
		purchase_user_assign = pur_Sudo.get_param('bi_assign_users_for_purchase.purchase_user_assign')
		res.update(
			draft_id=int(draft_id) or False,
			sent_id=int(sent_id) or False,
			purchase_order_id=int(purchase_order_id) or False,
			purchase_user_assign=purchase_user_assign,
			)
		return res

	def set_values(self):
		super(ResConfigInherit, self).set_values()
		purchase_assign_users = self.env['ir.config_parameter'].sudo()
		purchase_assign_users.set_param('bi_assign_users_for_purchase.draft_id',self.draft_id.id)
		purchase_assign_users.set_param('bi_assign_users_for_purchase.sent_id',self.sent_id.id)
		purchase_assign_users.set_param('bi_assign_users_for_purchase.purchase_order_id',self.purchase_order_id.id)
		purchase_assign_users.set_param('bi_assign_users_for_purchase.purchase_user_assign',self.purchase_user_assign)
	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: