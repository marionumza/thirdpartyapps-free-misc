# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Table Row Hover And Selected Highlight
#
###################################################################################

{
    'name': 'Table Row Hover And Selected Highlight',
    'version': '15.0.1.0.1',
    'summary': """ 
            Cybernetics Plus Tools Table Row Hover And Selected Highlight
            .""",
    'description': """ 
            Cybernetics Plus Tools Table Row Hover And Selected Highlight
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
    'depends': ['web'],
    'contributors': [
        'Developer <dev@cybernetics.plus>',
    ],
    'assets': {
        'web.assets_backend': [
            'ctp_table_row_highlight/static/src/css/style.css',
            'ctp_table_row_highlight/static/src/js/web.js',
        ],
    }
}
