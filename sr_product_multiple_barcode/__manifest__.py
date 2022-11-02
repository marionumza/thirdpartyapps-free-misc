# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

{
    'name': "Multiple Barcodes For Product",
    'version': "15.0.0.0",
    'summary': "You can register multiple barcode for single product and also select products in sale, purchase, invoice,  ETC... with that multiple barcode",
    'category': 'Sales',
    'description': """
    You can register multiple barcode for single product and also select products in sale, purchase, invoice,  ETC... with that multiple barcode
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_product.xml',
        'wizard/sr_import_multi_barcode.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/E8mrNKGNdoE',
    'images': ['static/description/banner.png'],
    "price": 0.0,
    "currency": 'EUR',
    
}
