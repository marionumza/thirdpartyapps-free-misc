# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import logging
import json

from pywebpush import webpush, WebPushException
from datetime import timedelta
from typing import List, Tuple, Optional, Any, Union, Dict
from requests import Response
from requests.exceptions import RequestException
from threading import Thread

from odoo import models, api

_logger = logging.getLogger(__name__)

PushResponseType = Dict[int, Response]
OdooDomainType = List[Optional[Tuple[str, str, Any]]]


class WebPushAPI(models.AbstractModel):
    _name = 'web_push.api'
    _description = 'Web Push API'

    @api.model
    def _push(
            self,
            data: str,
            domain: OdooDomainType,
            vapid_private_key: str,
            vapid_claims: dict[str, Any],
            timeout: Union[int, float],
            ttl: int,
    ):
        responses: PushResponseType = {}
        subscriber_env = self.env['web_push.subscriber']

        success_count = 0
        error_count = 0

        for subscriber_id in subscriber_env.search(domain):
            try:
                subscription: dict = json.loads(subscriber_id.subscription)
                response = webpush(
                    subscription_info=subscription,
                    vapid_private_key=vapid_private_key,
                    vapid_claims=vapid_claims.copy(),
                    timeout=timeout,
                    ttl=ttl,
                    data=data,
                )
            except (WebPushException, RequestException) as ex:
                _logger.warning(ex)
                responses[subscriber_id.id] = ex.response
                error_count += 1
            else:
                responses[subscriber_id.id] = response
                success_count += 1

        _logger.info(f'Success: {success_count}; Error: {error_count}')

        return responses

    @api.model
    def push(
            self,
            data: dict[str, Any],
            subscriber_domain: OdooDomainType = None,
            subject_email: str = None,
            audience: str = None,
            expiration: int = None,
            timeout: [int, float] = None,
            ttl: Union[int, timedelta] = 0,
    ) -> PushResponseType:
        """
        Send Web Push notification
        >>>
        ... # data structure
        ...{
        ...    'title': str,
        ...    'body': str,
        ...    'icon': str,
        ...    'data': dict,
        ...    'actions': [{
        ...        'action': str,
        ...        'title': str,
        ...        'icon': str,
        ...    }],
        ...}
        >>>
        """

        if subscriber_domain is None:
            subscriber_domain = []

        company = self.env.company

        if subject_email is None:
            subject_email = company.email

        vapid_id = self.env.ref('web_push_base.default_vapid')
        vapid_claims = {'sub': f"mailto: <{subject_email}>"}

        if audience:
            vapid_claims.update(aud=audience)
        if expiration:
            vapid_claims.update(exp=expiration)

        data = {
            'title': company.name,
            'icon': f'/web/content/{company._name}/{company.id}/logo',
            'actions': [],
            'data': {},
            **data
        }

        if 'defaultURL' not in data['data']:
            data['data']['defaultURL'] = company.get_base_url()

        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())

        response = self._push(
            vapid_private_key=vapid_id.private_key,
            vapid_claims=vapid_claims,
            timeout=timeout,
            ttl=ttl,
            data=json.dumps(data),
            domain=subscriber_domain,
        )

        return response

    @api.model
    def _threaded_push_callback(self, *args, **kwargs):
        with api.Environment.manage():
            with self.pool.cursor() as cr:
                return self.with_env(self.env(cr=cr)).push(*args, **kwargs)

    @api.model
    def threaded_push(
            self,
            data: dict[str, Any],
            subscriber_domain: OdooDomainType = None,
            subject_email: str = None,
            audience: str = None,
            expiration: int = None,
            timeout: [int, float] = None,
            ttl: Union[int, timedelta] = 0,
    ) -> None:
        """
        Send Web Push notification in another thread
        """
        self.env['web_push.subscriber'].flush()
        push_thread = Thread(
            name='Web Push',
            target=self._threaded_push_callback,
            kwargs=dict(
                data=data,
                subscriber_domain=subscriber_domain,
                subject_email=subject_email,
                audience=audience,
                expiration=expiration,
                timeout=timeout,
                ttl=ttl,
            ),
        )
        push_thread.start()
