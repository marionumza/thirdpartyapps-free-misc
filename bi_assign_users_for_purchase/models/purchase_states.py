# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError, Warning


class PurchaseOrderInherit(models.Model):
	_inherit = 'purchase.order'

	salesperson_id = fields.Many2one('res.users', compute="_compute_salesperson", store=True, string = 'Salesperson')
	auto_user_assign = fields.Boolean(string="Auto User Assign")

	@api.depends('state')
	def _compute_salesperson(self):
		for res in self:
			if res.auto_user_assign != False:
				if res.state == 'draft':
					res.salesperson_id = int(res.env['ir.config_parameter'].sudo().get_param('bi_assign_users_for_purchase.draft_id'))
					res.write({'user_id' : res.salesperson_id.id
						})
				elif res.state == 'sent':
					res.salesperson_id = int(res.env['ir.config_parameter'].sudo().get_param('bi_assign_users_for_purchase.sent_id'))
					res.write({'user_id' : res.salesperson_id.id
						})
				else:
					res.salesperson_id = int(res.env['ir.config_parameter'].sudo().get_param('bi_assign_users_for_purchase.purchase_order_id'))
					res.write({'user_id' : res.salesperson_id.id
						})
				sus_id = res.env['res.partner'].browse(SUPERUSER_ID)
				partner_email = res.partner_id.email
				if not partner_email:
						raise UserError(_('%s customer has no email id please enter email address')
								% (res.partner_id.name))
				else:
					template_id = self.env['ir.model.data']._xmlid_to_res_id('bi_assign_users_for_purchase.email_template_edi_salesperson_assigned', raise_if_not_found=False)
					
					template_browse = self.env['mail.template'].browse(template_id)
					if template_browse:
						values = template_browse.generate_email(res.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date','attachment_ids'])
						values['email_from'] = sus_id.email
						values['email_to'] = res.salesperson_id.email
						values['res_id'] = False
						values['author_id'] = self.env['res.users'].browse(self.env['res.users']._context['uid']).partner_id.id 
						if not values['email_to'] and not values['email_from']:
							pass
						msg_id = self.env['mail.mail'].create({
							'email_to': values['email_to'],
							'auto_delete': True,
							'email_from':values['email_from'],})
						mail_mail_obj = self.env['mail.mail']
						if msg_id:
							mail_mail_obj.sudo().send(msg_id)

			return True
	
	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
