# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.fields import datetime,date


class MinutesOfMeeting(models.Model):
    _inherit = 'calendar.event'
    
    def _get_lead_count(self):
        count = self.env['crm.lead'].search_count([('calendar_event_id','=',self.id)])
        self.lead_count = count
        
    description = fields.Text(string="Agenda")
    action_items = fields.Html(string="Action Item")
    conclusion = fields.Html(string="Conclusion")
    meeting_organizer = fields.Many2one('res.partner',string="Meeting Organizer")
    lead_count = fields.Integer(string="Lead", compute='_get_lead_count')
    
    def print_mom(self):
        return self.env.ref('minutes_of_meeting.report_pint_mom').report_action(self)
    
    def lead(self):
        return {
                'type': 'ir.actions.act_window',
                'domain':[('calendar_event_id','=',self.id)],
                'name': 'CRM Lead',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',
                'context': {'default_calendar_event_id': self.id}
        }
    def email_mom(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('minutes_of_meeting', 'email_template_mom')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id =  False
        ctx = {
            'default_model': 'calendar.event',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
            'default_partner_ids':[[6, False,self.partner_ids.ids]]
            }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

class CrmInherit(models.Model):
    _inherit = 'crm.lead'
   
    calendar_event_id = fields.Many2one('calendar.event', string="Meeting")
    