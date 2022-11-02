# -*- coding: utf-8 -*-

{
    'name': 'Company Description Field',
    'version': '1.0.0.1',
    'summary': """New field Description in the Company Form""",
    'description': """New field Description in the Company Form""",
    'category': 'Base',
    'author': 'bisolv',
    'website': "",
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['base'],

    'data': [
        'views/res_company.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
