# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields
from odoo.addons.web_push_base.web_push import generate_vapid
from odoo.exceptions import AccessError


class WebPushVAPID(models.Model):
    _name = 'web_push.vapid'
    _description = 'Web Push VAPID'

    public_key = fields.Char(required=True)
    private_key = fields.Char(required=True)
    subscriber_ids = fields.One2many(
        comodel_name='web_push.subscriber',
        inverse_name='vapid_id',
    )

    def create(self, values):
        rec_id = super(WebPushVAPID, self).create(values)
        empty = 'empty'
        if rec_id.private_key == empty or rec_id.public_key == empty:
            rec_id.generate_new_vapid()
        return rec_id

    def generate_new_vapid(self):
        self.subscriber_ids.unlink()
        self.private_key, self.public_key = generate_vapid()

    def unlink(self):
        default_vapid_id = self.env.ref('web_push_base.default_vapid')
        for rec_id in self:
            if rec_id == default_vapid_id:
                raise AccessError('Default vapid can not be deleted!')
        return super(WebPushVAPID, self).unlink()
