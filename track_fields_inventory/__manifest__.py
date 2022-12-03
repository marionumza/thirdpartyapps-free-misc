# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Show Edit History of Inventory',
    'author': 'Altela Softwares',
    'version': '15.0.1.0.0',
    'summary': 'Create history into chatter after editing inventory',
    'license': 'LGPL-3',
    'sequence': 1,
    'description': """Create history into chatter after editing inventory""",
    'category': 'Extra Tools',
    'website': 'https://www.altela.net',
    'depends': [
        'stock',
    ],
    'images': [
        'static/description/assets/banner.gif',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
