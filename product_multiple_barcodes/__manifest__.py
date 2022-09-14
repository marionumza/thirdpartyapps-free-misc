# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Multiple Barcodes',
    "version": "13.0.1.2.1",
    'author': 'VentorTech',
    'website': 'https://ventor.tech/',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/main_banner.png'],
    'summary': 'Allows to define multiple additional barcodes for products and to search products by additional barcodes and internal reference.',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/multiply_barcode_wizard.xml',
        'views/product_template_views.xml',
    ],
}
