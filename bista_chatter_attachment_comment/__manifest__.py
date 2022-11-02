# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Chatter Attachment Comment',
    "author": "Bista Solutions",
    "images": ['static/description/Chatter_Attachment_Comment.jpg'],
    "website": "https://www.bistasolutions.com",
    "support": "support@bistasolutions.com",
    'version': '15.0.1',
    'depends': ['base', 'mail'],
    'summary': "Chatter Attachment Comment",
    'description': """
        This is a full-featured chatter attachment system.
        ========================================
        
        It supports:
        ------------
            - Chatter attachment comment add and update functionality
    """,
    'category': 'Attachment',
    'demo': [
    ],
    'data': [
        'views/ir_attachment_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'bista_chatter_attachment_comment/static/src/models/attachment/attachment.js',
            'bista_chatter_attachment_comment/static/src/models/thread/thread.js',
            'bista_chatter_attachment_comment/static/src/widgets/form_renderer/form_renderer.js',
            'bista_chatter_attachment_comment/static/src/components/attachment_card/attachment_card.js',
            'bista_chatter_attachment_comment/static/src/components/attachment_image/attachment_image.js',
            'bista_chatter_attachment_comment/static/src/components/attachment_card/attachment_card.scss',
            'bista_chatter_attachment_comment/static/src/components/attachment_image/attachment_image.scss',
        ],
        'web.qunit_suite_tests': [
        ],
        'web.assets_qweb': [
            'bista_chatter_attachment_comment/static/src/components/attachment_card/attachment_card.xml',
            'bista_chatter_attachment_comment/static/src/components/attachment_image/attachment_image.xml',
        ],
    },
    'license': 'LGPL-3',
}

