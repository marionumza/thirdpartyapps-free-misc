# -*- coding: utf-8 -*-

{
    'name': "POS Direct Login",

    'summary': """
        Helps to directly login to POS.""",

    'description': """
        Log in to configured POS shop to save time.""",

    'author': "Odoo Being",
    'website': "https://www.odoobeing.com",
    'license': 'AGPL-3',
    'category': 'Point of Sale',
    'version': '15.0.1.0.0',
    'support': 'odoobeing@gmail.com',
    'images': ['static/description/images/pos_direct_login.png'],
    'installable': True,
    'auto_install': False,
    'depends': ['point_of_sale'],
    'data': [
        'views/res_users.xml',
    ],
}
