# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from typing import Any, Union

from odoo import models, fields, api
from odoo.addons.web_push_base.web_push import Subscription

SubscriptionType = Union[str, dict, Subscription]


class WebPushSubscriber(models.Model):
    _name = 'web_push.subscriber'
    _description = 'Web Push Subscriber'

    def _default_subscriber_name(self):
        return self.env['ir.sequence'].next_by_code('web_push_base.subscriber')

    name = fields.Char(
        required=True,
        readonly=True,
        default=_default_subscriber_name
    )
    subscription = fields.Text(
        default='{}',
        required=True,
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        readonly=True,
    )
    vapid_id = fields.Many2one(
        comodel_name='web_push.vapid',
        ondelete='cascade'
    )
    hash = fields.Char(
        compute='_compute_hash',
        store=True,
    )
    active = fields.Boolean(default=True)

    def create(self, values):
        self._update_values_subscription(values)
        return super(WebPushSubscriber, self).create(values)

    def write(self, values):
        self._update_values_subscription(values)
        return super(WebPushSubscriber, self).write(values)

    @classmethod
    def _update_values_subscription(cls, values: dict[str, Any]) -> None:
        subscription: SubscriptionType = values.get('subscription')

        if not subscription:
            return None

        if isinstance(subscription, dict):
            subscription = Subscription.from_dict(subscription)

        if isinstance(subscription, Subscription):
            values.update(subscription=subscription.to_json())

    @api.depends('subscription')
    def _compute_hash(self):
        def sub2hash(sub: str) -> str:
            return Subscription.from_string(sub).to_md5_digest().hex()

        for rec in self:
            rec.hash = sub2hash(rec.subscription) if rec.subscription else ''

    def _exists_by_hash(self, subscription_hash: str) -> bool:
        self.env.cr.execute("""
        SELECT EXISTS (
            SELECT 1 FROM web_push_subscriber WHERE hash=%s AND active
        )
        """, (subscription_hash,))
        return self.env.cr.fetchone()[0]

    @classmethod
    def _parse_subscription(
            cls,
            subscription: SubscriptionType,
    ) -> Subscription:
        if isinstance(subscription, dict):
            return Subscription.from_dict(subscription)
        if isinstance(subscription, str):
            return Subscription.from_string(subscription)
        return subscription

    def get_subscription(self) -> Subscription:
        return Subscription.from_string(self.subscription)

    @api.model
    def is_subscriber_available(self, subscription: SubscriptionType) -> bool:
        subscription = self._parse_subscription(subscription)
        return self._exists_by_hash(subscription.to_md5_digest().hex())

    @api.model
    def search_by_hash(self, subscription: dict = None, hash_value: str = None):
        if subscription:
            subscription = self._parse_subscription(subscription)
            hash_value = subscription.to_md5_digest().hex()
        return self.env[self._name].search([('hash', '=', hash_value)])
