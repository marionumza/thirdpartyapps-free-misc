from datetime import datetime
from odoo import api, models, SUPERUSER_ID


class ReminderVisa(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def work_anniversary_reminder(self):
        today = datetime.now()
        for i in self.env['hr.employee'].search([]):
            if i.service_start_date:
                daymonth = datetime.strptime(str(i.service_start_date), "%Y-%m-%d").date()
                print(daymonth)
                if today.day == daymonth.day and today.month == daymonth.month:
                    self.send_anniversary_notification(i.id)

    @api.model
    def send_anniversary_notification(self, emp_id):
        template_id = self.env['ir.model.data']._xmlid_to_res_id('work_anniversary_notification.work_anniversary_notification', raise_if_not_found=False)
        template_browse = self.env['mail.template'].browse(template_id)
        if template_browse:
            values = template_browse.generate_email(emp_id, ['subject', 'email_from', 'email_to'])
            values['email_to'] = self.env['hr.employee'].browse(emp_id).work_email
            values['email_from'] = self.env['res.partner'].browse(SUPERUSER_ID).email
            values['res_id'] = False
            if not values['email_to'] and not values['email_from']:
                pass
            msg_id = self.env['mail.mail'].create(values)
            if msg_id:
                self.env['mail.mail'].send(msg_id)
            return True
