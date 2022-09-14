# -*- coding: utf-8 -*-
# Copyright 2020 Hipernike, S.A.

{
    'name': 'User Access Expiration',
    'summary': 'Allow to set account expiration date for users',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'author': 'Hipernike, S.A.',
    'support': 'info@hipernike.com',
    'license': 'AGPL-3',
    'website': 'http://hipernike.com',
    'price': 0.00,
    'currency': 'EUR',
    'depends': [
        'base',
    ],
    'data': [
        'data/data.xml',
        'views/res_users_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'application': False,
    'installable': True,
}
