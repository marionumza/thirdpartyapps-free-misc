# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

{
    'name': 'SprintIT Customer Asset',
    'version': '14.0',
    'license': 'Other proprietary',
    'category': 'Field Service',
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'http://www.sprintit.fi',
    'depends': [
        'product',
        'sale_stock',
        'industry_fsm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_asset_views.xml',
        'views/fsm_views.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    "external_dependencies": {  # python pip packages
        #     'python': ['suds', 'dateutil'],
    },
    'images': ['static/description/cover.jpg', ],
    'installable': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',
}
