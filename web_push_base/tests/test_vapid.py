# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from pytest import mark
from ..web_push import generate_vapid


@mark.web_push
def test_generate_vapid():
    pv_key, pub_key = generate_vapid()
    assert isinstance(pv_key, str)
    assert isinstance(pub_key, str)
    assert len(pv_key) > 5
    assert len(pub_key) > 5
