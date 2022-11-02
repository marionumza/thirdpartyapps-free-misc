{
    'name': "Code Live",

    'summary': """
Provide features to write the code directly on the system
    """,

    'description': """
What it does
============
* Provide features to write the code directly on the system
Editions Supported
==================
1. Community Edition
2. Enterprise Edition
    """,

    'author': "Mountain",
    'support': "mountaintran2021@gmail.com",
    'category': 'Tools',
    'version': '0.1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/code_live_views.xml',
    ],
    'images' : [
        'static/description/background.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
