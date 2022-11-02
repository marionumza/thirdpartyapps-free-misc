# Copyright 2021-22 Manish Kumar Bohra <manishkumarbohra@outlook.com>
# License LGPL-3 - See http://www.gnu.org/licenses/Lgpl-3.0.html

{
    'name': 'Customer Pivot View',
    'version': '1.0',
    'summary': 'This module allows add pivot view in Contact Module',
    'description': 'This module allows add pivot view in Contact Module',
    'category': 'Other',
    'author': 'Manish Bohra',
    'website': 'www.linkedin.com/in/manishkumarbohra',
    'maintainer': 'Manish Bohra',
    'support': 'manishkumarbohra@outlook.com',
    'sequence': '10',
    'license': 'LGPL-3',
    "data": [
        'views/customer_pivot_view.xml',
    ],
    'images': ['static/description/mkb_customer_pivot.png'],
    'depends': ['contacts'],
    'installable': True,
    'auto_install': False,
    'application': True,
}


