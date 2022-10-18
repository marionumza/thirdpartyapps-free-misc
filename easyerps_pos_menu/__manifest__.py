# -*- coding: utf-8 -*-
{
    'name': "POS Menu",
    'support': "support@easyerps.com",
    'license': "LGPL-3",
    'summary': """
        PoS Menu
        """,

    'author': "Easyerps",
    'website': "https://EasyERPS.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

     'assets': {
        'point_of_sale.assets': [
            'easyerps_pos_menu/static/src/css/custom.css',
            'easyerps_pos_menu/static/src/js/PosMenu.js',
            'easyerps_pos_menu/static/src/js/Screen/chrome.js',
            'easyerps_pos_menu/static/src/js/Screen/TicketButton.js',
            'easyerps_pos_menu/static/src/js/Screen/CashMoveButton.js',
        ],
        'web.assets_qweb':[
            'easyerps_pos_menu/static/src/xml/PosMenu.xml',
            'easyerps_pos_menu/static/src/xml/chrome.xml',
            'easyerps_pos_menu/static/src/xml/TicketButton.xml',
        ],
    },
    'images': ['images/main_screenshot.png'],
}
