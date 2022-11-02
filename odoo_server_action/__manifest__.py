# -*- coding: utf-8 -*-

{
    'name': 'Server Actions',
    'version': '1.0.0.2',
    'summary': """Server Actions. Start / Stop / Restart""",
    'description': """""",
    'category': 'Extra Tools',
    'author': 'bisolv',
    'website': "www.bisolv.com",
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['base'],

    'data': [
        'security/server_action_security.xml',
        'security/ir.model.access.csv',
        'views/server_action_views.xml',
        'wizard/wizard_view.xml',
    ],

    'external_dependencies': {
        'python': ['paramiko'],
    },

    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
