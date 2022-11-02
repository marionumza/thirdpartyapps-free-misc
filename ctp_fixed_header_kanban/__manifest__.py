# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Cybernetics Plus Co., Ltd. Sticky Header Kanban Displaying View within Odoo.
#
###################################################################################

{
    'name': 'Sticky Header in Kanban',
    'version': '15.0.0.0.1',
    'summary': """ 
            Cybernetics Plus Co., Ltd. Sticky Header Kanban Displaying View within Odoo.
            """,
    'description': """ 
            Cybernetics Plus Co., Ltd. Sticky Header Kanban Displaying View within Odoo.
            """,
    'author': 'Cybernetics Plus Co., Ltd.',
    'website': 'https://www.cybernetics.plus',
    'live_test_url': 'https://www.cybernetics.plus',
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'contributors': [
        'Developer <dev@cybernetics.plus>',
    ],
    'assets': {
        "web.assets_backend": [
            'ctp_fixed_header_kanban/static/src/scss/kanban.scss',
        ],
    },
}
