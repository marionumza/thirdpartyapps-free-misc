import xmlrpc.client
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class adding_join(models.Model):
    _inherit = 'calendar.event'
    join_id = fields.Char()


class calender_event(models.Model):
    _inherit = 'hotel_management_module.users'
    _description = 'hotel_management_module.users'

    @api.model
    def create(self, values):
        if values.get('join_id', '1') == '1':
            values['join_id'] = self.env['ir.sequence'].next_by_code('hotel_management_module.users') or '1'

        self.api_request(values['name'], values['from_date'], values['to_date'], values['join_id'])
        record = super(calender_event, self).create(values)
        return record

    def api_request(self, name, from_date, to_date, join_id):
        if name:
            url = 'http://localhost:8069'
            db = 'mydb'
            username = 'admin'
            password = 'admin'
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            common.version()
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

            new_event = models.execute_kw(db, uid, password, 'calendar.event', 'create', [{
                'name': name, 'start': from_date, 'stop': to_date, 'join_id': join_id
            }])
            if not new_event: raise Exception
        else:
            raise ValidationError("Please fill the form Correctly")

    def unlink(self):

        if self.name:
            url = 'http://localhost:8069'
            db = 'mydb'
            username = 'admin'
            password = 'admin'
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            common.version()
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            id = models.execute_kw(db, uid, password, 'calendar.event', 'search', [[['join_id', '=', self.join_id]]])
            unlink_event = models.execute_kw(db, uid, password, 'calendar.event', 'unlink', [id])
            if not unlink_event: raise Exception

        return super(calender_event, self).unlink()

