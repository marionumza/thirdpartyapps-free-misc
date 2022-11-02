# -*- coding: utf-8 -*-
from odoo import http

from odoo.addons.web.controllers.main import Home, Session
from odoo.http import request
from odoo.fields import Datetime


class HomeInherit(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        res = super(HomeInherit, self).web_login(redirect=None, **kw)
        if request.params['login_success']:
            user = request.env['res.users'].sudo().search([('login', '=', kw['login'])], limit=1)
            if user:
                user.status = 'done'
                ICPSudo = request.env['ir.config_parameter'].sudo()
                need_to_store = ICPSudo.get_param('user_login_status.store_user_time')
                if need_to_store:
                    request.env['res.users.logger'].sudo().create({
                        'username': user.id,
                        'login_time': Datetime.now()
                    })
        return res


class SessionInherit(Session):
    @http.route()
    def logout(self, redirect='/web'):
        user = request.env['res.users'].sudo().search([('id', '=', request.session.uid)], limit=1)
        if user:
            user.status = 'blocked'
            ICPSudo = request.env['ir.config_parameter'].sudo()
            need_to_store = ICPSudo.get_param('user_login_status.store_user_time')
            if need_to_store:
                record = request.env['res.users.logger'].sudo().search(
                    [('username', '=', user.id), ('logout_time', '=', False)], limit=1)
                if record:
                    record.logout_time = Datetime.now()
        return super(SessionInherit, self).logout(redirect=redirect)
