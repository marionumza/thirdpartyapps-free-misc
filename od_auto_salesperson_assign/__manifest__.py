# -*- coding: utf-8 -*-
{
    'name': 'Auto Salesperson Assign',
    'summary': 'Assign Salesperson to Sale Orders and Ecommerce Orders',
    'version': '15.0.0.1',
    'description': 'This module helps to assign salesperson automatically based upon the configuration in eCommerce orders and direct sale orders.',
    'author': 'Odoo Decoder',
    'category': 'eCommerce',
    'website': 'https://odoodecoder.odoo.com/',
    'depends': ['website_sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/qkNXe0EGrgA',
}
