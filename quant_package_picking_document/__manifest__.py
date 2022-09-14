# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Package in Picking Document',
    'version': '13.0.0.1',
    'author': 'Global Resource Systems',
    'website': 'https://www.grs.ma',
    'license': 'LGPL-3',
    'summary': 'Showing all the packages of the picking in the picking document',
    'description': """
    This module show a table of packages related to the picking in Delivery Slip (Document)
    =======================================================================================

    The table show all the packages of the picking with their dimensions, shipping weight and gross weight.
    
    The package table is shown in the document only if the picking have packages related to it and the picking state is done.
    
    
    """,
    'depends': ['quant_package_dimensions'],
    'category': 'Inventory',
    'sequence': 13,
    'demo': [],
    'data': [
        'views/stock_picking_report_extra.xml',
    ],
    'qweb': [],
    'images': ['static/img/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}