# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'STOCK Kanban View',
    'version': '15.0.1.0.0',
    'summary': """
        Design Kanban View, New Style Kanban View, Web Responsive Kanban View, Advanced Kanban View, 
        Responsive STOCK Kanban View, Stock KanbanView, Responsive Stock Card View, Advanced Stock CardView, 
        Ouasmi Anas created the kanban view for odoo version 15., 
    """,
    'description': "Edit and Design new view kanban  offers an amazing view of Stock details.",
    'author': 'OUASMI ANAS',
    'category': 'Kanban_design',
    'maintainer': 'OUASMI ANAS',
    'price': '0',
    'currency': 'USD',
    'license': 'OPL-1',
    'images': [
        "static/description/banner.gif",
    ],
    'depends': [
        'base', 'stock',
    ],
    'data': [
        'views/card.xml',
    ],

    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [

    ],
}
