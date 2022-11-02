# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Show Home Backend Search Box
#
###################################################################################

{
    'name': 'Show Home Backend Search Box',
    'version': '15.0.1.0.1',
    'summary': """ 
            Cybernetics Plus Tools Show Home Backend Search Box
            .""",
    'description': """ 
            Cybernetics Plus Tools Show Home Backend Search Box
            .""",
    'author': 'Cybernetics Plus Co., Ltd.',
    'website': 'https://www.cybernetics.plus',
    'live_test_url': 'https://www.cybernetics.plus',
    'images': ['static/description/banner.png'],
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'contributors': [
        'Developer <dev@cybernetics.plus>',
    ],
    'depends': ['base'],
    'assets': {
        'web.assets_backend': [
            'ctp_show_search_box/static/src/js/search_box.js',
        ],
    },
}
