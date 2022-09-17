# -*- coding: utf-8 -*-
{
    'name': "Reportes Minimalisticos Argentina",

    'summary': """
        Reportes minimalisticos para documentos argentinos
    """,

    'description': """
        Reportes minimalisticos para documentos argentinos
        - Invoice
        - Sale Order
        - Purchase Order
        - Picking
    """,

    'author': "TRIXServer.com",
    'website': "https://TRIXServer.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_ar',],

    # always loaded
    'data': [
        'views/templates.xml',
    ],

    'installable' : True,
}
