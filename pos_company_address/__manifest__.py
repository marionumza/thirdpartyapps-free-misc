# -*- coding: utf-8 -*-
{
    'name': "pos_company_address",

    'summary': """
        Company Address in pos receipt""",

    'description': """
        Long description of module's purpose
    """,

    'author': "KIANANDA",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point of sale',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_company_address/static/src/js/*.js',
        ],
        'web.assets_qweb': [
            'pos_company_address/static/src/xml/**/*',
        ],

    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',

}
