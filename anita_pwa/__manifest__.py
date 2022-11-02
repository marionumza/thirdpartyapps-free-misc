# -*- coding: utf-8 -*-
{
    'name': "anita_pwa",

    'summary': """
        anita pwa support for odoo
    """,

    'description': """
        anita pwa support for odoo,
        funenc,
        anita odoo,
        anita pwa,
        anita pwa theme,
        anita pwa odoo,
        anita multi tab theme,
        anita
    """,

    'author': "Funenc",
    'website': "http://en.funenc.com",
    'license': "OPL-1",
    'live_test_url': 'https://en.funenc.com/',

    'images': ['static/description/awesome_description.gif'],

    'category': 'App/pwa',
    'version': '15.0.0.2',

    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/anita_web.xml',
        'views/anita_pwa_manifest.xml',
        'views/anita_pwa_setting.xml',
        'views/anita_pwa_service_worker.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'anita_pwa/static/src/user_menu_patch.js',
        ],
        'web.assets_qweb': [],
        'web.assets_backend_prod_only': []
    }
}
