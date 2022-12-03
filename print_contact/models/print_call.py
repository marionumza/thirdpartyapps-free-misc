from odoo import api,fields,models


class extend_contact(models.Model):
    _inherit='res.partner'
    
    def print_page(self):
        return self.env.ref('print_contact.action_report_page').report_action(self)
    
    def print_listing(self):
        return self.env.ref('print_contact.action_report_listing').report_action(self)
    
    def print_checkin(self):
        return self.env.ref('print_contact.action_report_checkin').report_action(self)
    
