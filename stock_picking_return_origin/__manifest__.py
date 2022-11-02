# -*- coding: utf-8 -*-
# Copyright 2021 Osis.

{
    'name': 'Stock picking return origin',
    'version': '15.0.0.1',
    'summary': 'Stock picking return information Origin',
    'category': 'Stock',
    'author': 'Osis',
    'website': 'https://www.osis.dz',
    'license': 'OPL-1',
    'depends': [
        'stock'
    ],
    'data': [

        'views/stock_picking.xml',
    ],
    "qweb": [],

    'installable': True,
    'auto_install': False,

    'external_dependencies': {
        'python': [],
    }
}
