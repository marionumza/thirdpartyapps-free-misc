# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from datetime import timedelta
from requests import Response
from pytest import mark

from odoo.tests import TransactionCase, tagged


@mark.web_push
@tagged('post_install', 'web_push')
class TestWebPushAPI(TransactionCase):

    def setUp(self):
        super(TestWebPushAPI, self).setUp()
        self.api_env = self.env['web_push.api']
        self.subscription = {
            "endpoint": "https://fcm.googleapis.com/fcm/send/eNXD",
            "expirationTime": None,
            "keys": {
                "auth": "kLCRMdAj6Cj98h3mpknpdA",
                "p256dh": "BK7osGtzH7InFETkdGhXlnnPdyTS83lydzrx2Ut1r0oV8dcDMkS4M5sdYdG6oJZRC3Iy-beUkM0Fm3xSvV6BLgo",
            }
        }
        self.vapid_id = self.env.ref('web_push_base.default_vapid')
        self.vapid_id.generate_new_vapid()
        self.subscriber_id = self.env['web_push.subscriber'].create({
            'subscription': self.subscription,
            'user_id': self.env.uid,
            'vapid_id': self.vapid_id.id
        })

    def test_push(self):
        data = {
            'title': 'Title',
            'body': 'Body',
            'data': {
                'link': '/'
            },
            'actions': [
                {
                    'title': 'Link Title',
                    'action': 'link'
                }
            ]
        }

        response_items = self.api_env.push(data, ttl=timedelta(minutes=1))

        self.assertEqual(len(response_items), 1)

        for sub_id, response in response_items.items():
            self.assertTrue(isinstance(sub_id, int))
            self.assertTrue(isinstance(response, Response))
            self.assertTrue(response.status_code == 404)
