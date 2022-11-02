# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Uncannycs LLP
#    Copyright (C) 2022 Uncannycs LLP (<http://uncannycs.com>).
#
##############################################################################

{
    "name": "Dynamic Terms And Conditions",
    "summary": """Dynamic Terms And Conditions""",
    "version": "15.0.0.0.0",
    'author': 'Uncanny Consulting Services LLP',
    'maintainer': 'Uncanny Consulting Services LLP',
    'website': 'http://www.uncannycs.com',
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_management", "account", "purchase", "contacts"],
    "data": [
        'views/res_company.xml',
        'views/res_config.xml',
        'views/res_country.xml',
        'report/sale_report.xml',
        'report/purchase_report.xml',
        'report/invoice_report.xml',
    ],
    'images': ['static/description/banner.gif'],
}
