
{
    'name': 'Access Card request',
    'category': 'Human Resources',
    'description': """
                   HR Requests for access card .
                 """,
    'summary': 'HR Requests for access card'
               ''
               ,
    'version': '15.0',
    'author': 'Israa Elkolaly',
    'images': [

    ],
    'depends': ['base','hr'
                ],
    'images': [],
    'data': [

        'security/groups_rules.xml',
        'views/access_card_views.xml',
        'views/templates.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',


    ],
    'demo': [],
    'images': ['static/description/icon.png'],

    'installable': True,
    'auto_install': False,
}
