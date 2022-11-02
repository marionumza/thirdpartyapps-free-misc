# -*- coding: utf-8 -*-

{
    'name': 'Employee Contract Types',
    'version': '1.0',
    'summary': """Employee Contract Types""",
    'category': 'Human Resources/Contracts',
    'category': 'Base',
    'author': 'bisolv',
    'website': "www.bisolv.com",
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['base', "hr_contract",

                ],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_contract_types.xml',
        'views/hr_contract.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
