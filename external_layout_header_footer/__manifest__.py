# -*- coding: utf-8 -*-
{
    'name': "External Layout For Header And Footer",

    'summary': """
        Extra Added Report Features""",

    'description': """
        This module using to customise External Layout For Header And Footer
    """,

    'author': "klystron Global",
    'website': "www.klystronglobal.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Report',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'reports/custom_header_footer.xml'

    ],
    'images':  ['static/description/logo.png'],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
