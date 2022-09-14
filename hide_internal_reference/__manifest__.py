# -*- coding: utf-8 -*-
{
    'name': "Hide Internal Reference",
    'summary': """
        Hide Product Internal Reference
        """,

    'description': """
        Currently in Odoo the product internal reference appear beside the product name beside sale order, invoice, etc.. 
        Like this "[CODE] Product Name". Using this module will hide the problematic.
    """,

    'author': "da Ti Soft Consulting",
    'website': "https://github.com/trinanda/",
    'images': ['static/description/icon.png'],
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Utilities',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
