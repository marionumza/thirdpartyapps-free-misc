# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _
from datetime import date

class ResPartner(models.Model):
    _inherit = "res.partner"

    date = fields.Date()
    recipients_of_email = fields.Many2many(comodel_name='res.partner',relation='customer',column1='partner_id',column2='partner_name',string = "Recipients of the Email")
    subject = fields.Text('Subject')
    email_content = fields.Text('Email Content')

    def send_email_from_customer(self):
        today_date = date.today()
        current_date = str(today_date)
        obj = self.env['res.partner'].search([])
        if obj:
            context = self._context
            current_uid = context.get('uid')
            current_login_user = self.env['res.users'].browse(current_uid)
            for customer in obj:
                email_to = []
                obj_date = str(customer.date)
                if customer and current_date == obj_date:
                    for record in customer.recipients_of_email:
                        if record.email:
                            email_to.append(record)
                    if email_to:
                        mail={
                              'subject'       : customer.subject,
                              'email_from'    : customer.email,
                              'recipient_ids' : [(6,0,[v.id for v in email_to])],
                              'body_html'     : customer.email_content,                  
                             }
                    if mail: 
                        mail_create = current_login_user.env['mail.mail'].create(mail)
                        if mail_create:
                            mail_create.send()
                            self.mail_id = mail_create
