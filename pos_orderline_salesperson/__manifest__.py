# -*- coding: utf-8 -*-
{
    'name': 'POS Orderline Salesperson',
    'version': '14.1.1.0',
    'summary': 'POS Orderline Salesperson',
    'category': 'Sales/Point Of Sale',
    'author': 'Zeinab Abdelmonem',
    'email': 'zeinababdelmonem9@gmail.com',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_orderline_salesperson/static/src/css/salesperson.css',
            'pos_orderline_salesperson/static/src/js/models.js',
            'pos_orderline_salesperson/static/src/js/orderline.js',
            'pos_orderline_salesperson/static/src/js/salesperson.js',
            'pos_orderline_salesperson/static/src/js/salespersonpopup.js',
        ],
        'web.assets_qweb': [
            'pos_orderline_salesperson/static/src/xml/**/*',
        ],
    },
    'images': [
        'static/description/click_button_to_open_wizard.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
