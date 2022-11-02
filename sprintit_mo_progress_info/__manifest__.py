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
    'name': 'MO Production Progress',
    'version': '0.1',
    'license': 'LGPL-3',
    'category': 'mrp',
    'description': '''Progress of MO on list view to display the number of workorder done till now.
                      Progress of Manufacturing Order workorders state workorder state''', 
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'http://www.sprintit.fi',
    'depends': [
        'mrp'
    ],
    'data': [
        'view/mrp_production_view.xml',
    ],
    'images': ['static/description/cover.jpg',],
    'installable': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',    
}

