# -*- coding: utf-8 -*-
{
    'name': "web login Verification Code",

    'summary': """
      企业版登录验证码
        """,
    'description': """
       企业版登录验证码
    """,

    'author': "yao",
    'website': "http://139.198.115.129:8069/",
    'category': 'Extra Tools',
    'version': '15.0.0.1',
    "license": "AGPL-3",
    'depends': ['web'],
    'installable': True,
    'auto_install': True,
    'external_dependencies': {'python': ['captcha']},
    'data': [
        'static/xml/login_inherit.xml'
    ],
    'images': ['static/description/01.png'],
}
