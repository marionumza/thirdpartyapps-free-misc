# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Product Multi Alias",
    'summary': 'Add more than one alias for your product and search on all odoo',
    "author": "Quilsoft",
    'category': 'Sales',
    "version": "13.0.1.0.0",
    'depends': ['product', 'sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'installable': True,
}