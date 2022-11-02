# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Customize Web Backend Title
#
###################################################################################

{
    'name': 'Customize Web Backend Title',
    'version': '15.0.1.0.1',
    'summary': """ 
            Cybernetics Plus Tools Customize Web Backend Title
            .""",
    'description': """ 
            Cybernetics Plus Tools Customize Web Backend Title
            .""",
    'author': 'Cybernetics Plus Co., Ltd.',
    'website': 'https://www.cybernetics.plus',
    'live_test_url': 'https://www.cybernetics.plus',
    'images': ['static/description/banner.png'],
    'category': 'Tools',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'contributors': [
        'Developer <dev@cybernetics.plus>',
    ],
    'depends': ['base_setup'],
    'demo': [
        'data/title_config.xml',
    ],
    'data': [
        'views/res_config.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ctp_customize_title/static/src/js/customize_title.js',
        ],
    },
}
