# -*- coding: utf-8 -*-
# Copyright 2021 Gusti Tammam

from odoo import api, SUPERUSER_ID
from odoo.exceptions import Warning


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    return True


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    return True
