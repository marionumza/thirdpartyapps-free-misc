# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from pytest import mark
from odoo.tests import TransactionCase, tagged


@mark.web_push
@tagged('post_install', 'web_push')
class TestWebPushVAPID(TransactionCase):

    def _create_default_vapid(self):
        return self.env['web_push.vapid'].create({
            'public_key': 'empty',
            'private_key': 'empty',
        })

    def setUp(self):
        super(TestWebPushVAPID, self).setUp()
        self.empty = 'empty'

    def test_default_vapid(self):
        vapid_id = self.env.ref('web_push_base.default_vapid', False)
        self.assertTrue(vapid_id)
        self.assertNotEqual(vapid_id.private_key, self.empty)
        self.assertNotEqual(vapid_id.public_key, self.empty)
        self.assertIsNotNone(vapid_id.public_key)
        self.assertIsNotNone(vapid_id.private_key)

    def test_create(self):
        vapid_id = self._create_default_vapid()
        self.assertNotEqual(vapid_id.public_key, self.empty)
        self.assertNotEqual(vapid_id.private_key, self.empty)
        self.assertIsNotNone(vapid_id.public_key)
        self.assertIsNotNone(vapid_id.private_key)

    def test_generate_new_vapid(self):
        vapid_id = self._create_default_vapid()
        vapid_id.generate_new_vapid()
        self.assertNotEqual(vapid_id.public_key, self.empty)
        self.assertNotEqual(vapid_id.private_key, self.empty)
        self.assertIsNotNone(vapid_id.public_key)
        self.assertIsNotNone(vapid_id.private_key)
