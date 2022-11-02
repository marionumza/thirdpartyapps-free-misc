# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class OdooServerAction(models.Model):
    _name = 'odoo.server.action'
    _description = 'Server Action'

    name = fields.Char('Action Name', required=True)
    host = fields.Char('Server URL', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    description = fields.Text('Description')
    timeout = fields.Integer('Timeout', default=30)

    command_start = fields.Char('Start Command', required=True)
    command_stop = fields.Char('Stop Command', required=True)
    command_restart = fields.Char('Restart Command', required=True)

    history_ids = fields.One2many('odoo.server.action.history', 'server_id')
    auto_delete_history_rotation = fields.Integer(string='Clean History Rotation', default=30, help="Histories will be deleted automaticlly if the number exceeds")

    def get_server_object(self):
        import paramiko

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()

            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(hostname=self.host, username=self.username, password=self.password, timeout=self.timeout)
            transport = client.get_transport()
            channel = transport.open_session()
            return {'status': 'success', 'object': channel}

        except Exception as e:
            return {'status': 'failed', 'exception': str(e)}

    def test_server_connection(self, raise_success=True, raise_failed=True):
        self.ensure_one()

        connection_data = self.get_server_object()

        if raise_success and connection_data['status'] == 'success':
            raise UserError("Successful connection !!\t")

        if raise_failed and connection_data['status'] == 'failed':
            raise UserError("Failed !!\nReason:\t" + str(connection_data['exception']))

    def action_start_server(self):
        self.ensure_one()
        self.test_server_connection(raise_success=False)
        connection_data = self.get_server_object()
        channel = connection_data['object']
        channel.exec_command(self.command_start)
        self.env['odoo.server.action.history'].create({'server_id': self.id, 'action': 'started'})
        self.rotate_history()
        return {
            'name': 'Success',
            'view_mode': 'form',
            'res_model': 'odoo.server.action.result.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_body': "Started %s successfully !!!" % self.name},
        }
    
    def action_stop_server(self):
        self.ensure_one()
        self.test_server_connection(raise_success=False)
        connection_data = self.get_server_object()
        channel = connection_data['object']
        channel.exec_command(self.command_stop)
        self.env['odoo.server.action.history'].create({'server_id': self.id, 'action': 'stopped'})
        self.rotate_history()
        return {
            'name': 'Success',
            'view_mode': 'form',
            'res_model': 'odoo.server.action.result.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_body': "Stopped %s successfully !!!" % self.name},
        }

    def action_restart_server(self):
        self.ensure_one()
        self.test_server_connection(raise_success=False)
        connection_data = self.get_server_object()
        channel = connection_data['object']
        channel.exec_command(self.command_restart)
        self.env['odoo.server.action.history'].create({'server_id': self.id, 'action': 'restarted'})
        self.rotate_history()
        return {
            'name': 'Success',
            'view_mode': 'form',
            'res_model': 'odoo.server.action.result.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_body': "Restarted %s successfully !!!" % self.name},
        }

    def rotate_history(self):
        self.ensure_one()
        rotation = self.auto_delete_history_rotation

        if len(self.history_ids) > rotation:

            unwanted = self.history_ids.sorted(key=lambda x: x.create_date, reverse=True)
            unwanted[rotation:].unlink()


class OdooServerActionHistory(models.Model):
    _name = 'odoo.server.action.history'

    server_id = fields.Many2one('odoo.server.action')
    action = fields.Selection([('started', 'Started'), ('stopped', 'Stopped'), ('restarted', 'Restarted'), ])

