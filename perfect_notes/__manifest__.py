# -*- coding: utf-8 -*-
{
    'name': "Perfect notes",
    'version': '15.0.2.1',
    'summary': 'Perfect notes',
    'description': """Perfect notes to odoo""",
    'category': 'Extra Tools',
    'author': "Codoo-erp",
    'website': "https://codoo-erp.com",
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/tags.xml',
        'views/category.xml',
        'views/subcategory.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto-install': False,
}
