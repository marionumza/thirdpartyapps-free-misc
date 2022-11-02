# -*- coding: UTF-8 -*-
# Copyright 2022 Solvve, Inc. <sales@solvve.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    'name': "Web Push Base",

    'summary': "Provided basic functionality for web push",

    'description': """
    """,

    'author': "Solvve Inc.",
    'website': "https://solvve.com",

    'category': 'Technical',
    'version': '15.0.0.6',
    'license': 'LGPL-3',

    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',
        'data/menuitem_data.xml',
        'data/web_push_vapid_data.xml',

        'views/web_push_subscriber_views.xml',
    ],

    'external_dependencies': {
        'python': [
            'pywebpush',
        ]
    },

    'assets': {
        'web.assets_backend': [
            'web_push_base/static/src/js/subscribe_systray.js',
            'web_push_base/static/src/js/subscription_item.js',
            'web_push_base/static/src/scss/*.scss',
        ],
        'web.assets_qweb': [
            'web_push_base/static/src/xml/*.xml',
        ],
        'web.tests_assets': [
            'web_push_base/static/tests/*.js'
        ]
    },

    'images': [
        'static/description/main_1.jpg',
        'static/description/main_screenshot.jpg',
    ],
}
