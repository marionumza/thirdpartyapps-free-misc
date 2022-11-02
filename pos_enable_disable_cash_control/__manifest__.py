# -*- coding: utf-8 -*-
{
    'name': "pos_enable_disable_cash_control",

    'summary': """
        pos_enable_disable_cash_control""",

    'description': """
        pos_enable_disable_cash_control
    """,

    'author': "Tri Nanda",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_config_view.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'pos_enable_disable_cash_control/static/src/xml/Popups/ClosePosPopup.xml',
        ],

    },
}
