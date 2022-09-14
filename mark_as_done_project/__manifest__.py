# -*- coding: utf-8 -*-
{
    'name': "Project Mark as Done",

    'summary': """
        Mark as Done, Archieve, complete, uncomplete""",

    'description': """
        Mark as Done, Archieve, Complete, Un Complete
    """,

    'author': "ticinoWEB",
    'website': "http://www.ticinoWEB.tech",

    'category': 'project',
    'version': '0.1',
   "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base','project','sale_timesheet'],
    'images': ['static/description/banner.png'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/buttons.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
