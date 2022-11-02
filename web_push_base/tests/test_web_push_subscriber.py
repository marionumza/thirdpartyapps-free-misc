# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from pytest import mark

from odoo.tests import TransactionCase, tagged
from ..web_push import Subscription


@mark.web_push
@tagged('post_install', 'web_push')
class TestWebPushSubscriber(TransactionCase):
    def setUp(self):
        super(TestWebPushSubscriber, self).setUp()
        self.subscription = {
            "endpoint": "https://fcm.googleapis.com/fcm/send/eN",
            "expirationTime": None,
            "keys": {
                "auth": "kL",
                "p256dh": "BK7",
            }
        }
        self.subscriber_env = self.env['web_push.subscriber']
        self.subscriber_id = self.subscriber_env.create({
            'subscription': self.subscription,
            'user_id': self.env.uid,
            'vapid_id': self.env.ref('web_push_base.default_vapid').id
        })

    def test_update_values_subscription(self):
        values = {'subscription': self.subscription}
        self.env['web_push.subscriber']._update_values_subscription(values)
        self.assertTrue(isinstance(values['subscription'], str))

    def test_compute_hash(self):
        self.assertTrue(isinstance(self.subscriber_id.hash, str))
        self.assertTrue(len(self.subscriber_id.hash) > 10)

    def test_is_subscriber_available(self):
        self.subscriber_env.flush()
        self.assertTrue(
            self.subscriber_env.is_subscriber_available(self.subscription)
        )

    def test_search_by_hash(self):
        sub_id = self.subscriber_env.search_by_hash(self.subscription)
        self.assertTrue(sub_id)

        sub_digest = Subscription.from_dict(self.subscription).to_md5_digest()
        sub_id = self.subscriber_env.search_by_hash(hash_value=sub_digest.hex())
        self.assertTrue(sub_id)
