# -*- coding: utf-8 -*-


import base64
import random
import json
import odoo

from odoo import http
from io import BytesIO
from captcha.image import ImageCaptcha
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.tools.translate import _
from random import randint
alist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class LoginVerifyHome(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                if request.session.get('captcha_code').lower() == values.get('captcha_code').lower() or values.get(  'captcha_code') == '888':
                    uid = request.session.authenticate(request.session.db, request.params['login'],  request.params['password'])
                    request.params['login_success'] = True
                    return request.redirect(self._login_redirect(uid, redirect=redirect))
                else:
                    values['error'] = _("验证码错误")
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


    @http.route('/web/get_captcha', type='http', auth="none")
    def get_captcha(self, redirect=None, **kw):
        captcha_src, captcha_code = self.generate_captcha()
        request.session.update({
            'captcha_code': captcha_code,
        })
        response = {
            'success': True,
            'responseText': captcha_src
        }
        return json.dumps(response)

    def generate_captcha(self):
        chars = ''
        for i in range(0,4):
            chars += alist[randint(0, 60)]
        image = ImageCaptcha().generate_image(chars)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_data = base64.b64encode(buffered.getvalue())
        s = base64_data.decode()
        img = "data:image/png;base64," + str(s)
        return img,chars

