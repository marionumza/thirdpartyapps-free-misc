# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from pytest import mark
from ..web_push import Subscription

subscription_dict = {
    "endpoint": "https://fcm.googleapis.com/fcm/send/eN",
    "expirationTime": None,
    "keys": {
        "auth": "kL",
        "p256dh": "BK7",
    }
}
subscription_string = """{
    "endpoint": "https://fcm.googleapis.com/fcm/send/eN",
    "expirationTime": null,"keys": {"auth": "kL","p256dh": "BK7"}
}"""


@mark.web_push
def test_subscription_parse():
    subscription = Subscription.from_dict(subscription_dict)
    assert isinstance(subscription, Subscription)
    assert subscription.keys
    assert subscription.expirationTime is None
    assert subscription.endpoint

    subscription = Subscription.from_string(subscription_string)
    assert isinstance(subscription, Subscription)
    assert subscription.keys
    assert subscription.expirationTime is None
    assert subscription.endpoint


@mark.web_push
def test_subscription_dump():
    subscription = Subscription.from_dict(subscription_dict)

    dump = subscription.to_dict()
    assert dump
    assert isinstance(dump, dict)

    dump = subscription.to_json()
    assert dump
    assert isinstance(dump, str)


@mark.web_push
def test_subscription_md5_digest():
    subscription = Subscription.from_dict(subscription_dict)
    digest = subscription.to_md5_digest()

    assert digest
    assert isinstance(digest, bytes)
