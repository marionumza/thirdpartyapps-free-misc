# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<https://sprintit.fi>).
#
##############################################################################


{
    'name': 'SprintIT Customer Portal Documents Access',
    'version': '15.0.1.0.0',
    'license': 'Other proprietary',
    'category': 'Portal',
    'description': 'Customer Portal Documents Access',
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'https://www.sprintit.fi',
    'images': ['static/description/cover.jpg',],
    'depends': [
        'portal',
    ],
    'data': [
        'views/res_partner.xml',
        'views/portal_templates.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    "external_dependencies": { # python pip packages
    #     'python': ['suds', 'dateutil'],
    },
    'installable': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',
 }

