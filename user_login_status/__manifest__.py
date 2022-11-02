# -*- coding: utf-8 -*-
{
    'name': "User Login/Logout Status",

    'summary': """""",

    'description': """
        User Login/Logout Status and User total Login Time Status viewer
    """,

    'author': "Md. Hossain Akash",
    'website': "https://mdakash.xyz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/setting.xml',
    ],
    'license': 'AGPL-3',
    # 'price': 5.0,
    # 'currency': 'USD'
}
