# -*- coding: utf-8 -*-
{
    'name': "Auto Deactivate Users",

    'summary': """
        This module deactivates employee's linked user once their contract expires""",

    'description': """
        This module will check for employees valid contracts and it will deactivate the employee linked user without deleting it, if there are no valid contracts. For any modification or custom functionality don't hesitate to contact us http://m.me/odoo.developer
    """,

    'author': "Barameg",
    'website': "http://www.barameg.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'price': 0.00,
    'currency':'USD'
}
