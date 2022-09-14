# -*- coding: utf-8 -*-
{
    'name': 'Product Tweaks. Multiple Internal Reference Product Code SKU',
    'version': '13.0.1.0',
    'author': 'Ivan Sokolov',
    'category': 'Sales',
    'license': 'GPL-3',
    'website': 'https://demo.promintek.com',
    'live_test_url': 'https://demo.promintek.com',
    'summary': """Multiple internal references for products """,
    'description': """
    Multiple Internal References SKU Product Codes
""",
    'depends': ['product', 'stock'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/prt_product.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
