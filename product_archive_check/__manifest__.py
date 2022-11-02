# -*- coding: utf-8 -*-
# Copyright 2021-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    'name': "Product Archive Check",
    'summary': """This Tiny App module do not let a product be archived if the Qty on hand is not 0.""",
    'version': '15.0.1.0.0',
    'category': 'Uncategorized',
    'website': "http://sodexis.com/",
    'author': "Sodexis",
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'images': ['images/main_screenshot.png'],
    'depends': [
        'product'
    ],
}