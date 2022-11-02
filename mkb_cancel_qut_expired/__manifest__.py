# Copyright 2020-22 Manish Kumar Bohra <manishkumarbohra@outlook.com>
# License LGPL-3 - See http://www.gnu.org/licenses/Lgpl-3.0.html

{
    'name': 'Cancel Expired Quotation',
    'version': '1.0.0',
    'summary': 'This module allows to cancel the expired quotations via cron action',
    'description': 'This module allows to cancel the expired quotations via cron action',
    'category': 'Sales',
    'author': 'Manish Bohra',
    'website': 'www.linkedin.com/in/manishkumarbohra',
    'maintainer': 'Manish Bohra',
    'support': 'manishkumarbohra@outlook.com',
    'sequence': '10',
    'license': 'LGPL-3',
    "data": [
        'data/cancel_qut_action.xml',
    ],
    'images': ['static/description/cancel_qut.png'],
    'depends': ['sale_management'],
    'installable': True,
    'auto_install': False,
    'application': True,
}


