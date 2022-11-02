# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Alerta en despachos parciales',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'description': '''
       Alerta en despachos parciales no confirmados.
    ''',
    'summary': 'Muestra alerta en los despachos parciales sin validar',
    'website': 'http://www.trescloud.com',
    'author': 'TRESCLOUD CIA LTDA',
    'maintainer': 'TRESCLOUD CIA. LTDA.',
    'license': 'OPL-1',
    'depends': ['base', 'stock', 'sale_management'],
    'data': [
        'views/stock_picking_view.xml'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "support": "soporte@trescloud.com",
    'images': [
        'static/description/banner_out.png',
        'static/description/icon.png',
        'static/description/config1.png',
        'static/description/config2.png',
        'static/description/banner.png'
    ],
}
