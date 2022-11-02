# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from py_vapid import b64urldecode
from typing import List, Union, Any

from odoo.http import Controller, route, request
from ..web_push import Subscription


class WebPushController(Controller):

    @route(
        '/web_push/unlink_by_hash',
        methods=['POST'],
        type='json',
        auth='public'
    )
    def unlink_subscriptions_by_hash(self, hash_items: List[str]) -> bool:
        if not hash_items:
            return False

        subscriber_ids = request.env['web_push.subscriber'].sudo().search([
            ('hash', 'in', hash_items)
        ])

        if subscriber_ids:
            subscriber_ids.unlink()
            return True
        else:
            return False

    @route('/web_push/subscribe', methods=['POST'], type='json', auth='public')
    def subscribe(self, subscription: dict) -> bool:
        subscriber_env = request.env['web_push.subscriber'].sudo()
        user_id = request.env.user
        vapid_id = request.env.ref('web_push_base.default_vapid')

        if subscriber_env.is_subscriber_available(subscription):
            return False

        subscriber_id = subscriber_env.create({
            'user_id': user_id.id,
            'subscription': subscription,
            'vapid_id': vapid_id.id,
        })

        request.env.cr.commit()
        request.env['web_push.api'].sudo().threaded_push({
            'body': 'Subscribed!',
        }, subscriber_domain=[('id', '=', subscriber_id.id)])

        return True

    @route('/web_push/unsubscribe', methods=['POST'], type='json', auth='public')
    def unsubscribe(self, subscription: dict) -> bool:
        subscriber_env = request.env['web_push.subscriber'].sudo()
        subscriber_ids = subscriber_env.search_by_hash(subscription)

        if not subscriber_ids:
            return False

        subscriber_ids.unlink()

        return True

    @route(
        '/web_push/public_key/<string:response_type>',
        methods=['POST'],
        type='json',
        auth='public',
    )
    def public_key(self, response_type) -> Union[str, List[int]]:
        supported_types = ('string', 'uint8_array')

        if response_type not in supported_types:
            raise TypeError(f'Supported types: {supported_types}')

        public_key = request.env.ref('web_push_base.default_vapid').sudo().public_key

        if response_type == 'uint8_array':
            return list(map(int, b64urldecode(public_key.encode())))

        if response_type == 'string':
            return public_key

    @route('/web_push/systray', methods=['POST'], type='json', auth='user')
    def systray(self, subscription: dict) -> dict[str, Any]:
        subscriber_env = request.env['web_push.subscriber']
        subscriber_items = subscriber_env.search_read(
            [
                ('user_id', '=', request.env.uid),
            ],
            fields=['name', 'hash', 'create_date'],
            limit=24,
            order='create_date desc',
        )

        if not subscription:
            return {
                'subscribed': False,
                'targetHash': '',
                'subscriberItems': subscriber_items,
            }

        target_hash = Subscription.from_dict(subscription).to_md5_digest().hex()
        return {
            'subscribed': subscriber_env.is_subscriber_available(subscription),
            'targetHash': target_hash,
            'subscriberItems': subscriber_items,
        }
