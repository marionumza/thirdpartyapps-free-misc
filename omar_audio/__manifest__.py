# -*- coding: utf-8 -*-
{
    'name': "Omar Audio Widget",
    'summary': "Free Custom Audio Widget made by Omar(Odoo developer at Diwan For Scientific Solutions) & Diwan For Scientific Solutions co",
    'author': "Diwan For Scientific Solutions Co",
    'website': "https://www.linkedin.com/in/omar-amr-zaky-923467145/",
    'category': "web",
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    'assets': {
            'web.assets_backend': [
                'omar_audio/static/js/omar_audio.js',
            ]
    },

    'images': [
        'static/description/audio_icon.jpg'
    ],
    # 'data': [
    #     'views/templates.xml',
    # ],
    'auto_install': False,

    'installable': True,
    'web_preload': True,

}