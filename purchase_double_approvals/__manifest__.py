# -*- coding: utf-8 -*-
{
    'name': "Purchase Double Approvals",

    'summary': """
        Adds Extra layer of validation in purchase request
        """,

    'description': """
        This module adds extra layer of workflow in stage where approval of purchase order will have to go through it
    """,

   'author': "10 Orbits",
    'website': "https://www.10orbits.com",
    
    'category': 'Purchase',
    'version': '15.0.1.0.0',

    'depends': ['purchase'],
    
    'data': [
        'data/approvals_security.xml',
        'views/initial_approval_view.xml',
    ],
    'images': ['static/description/Banner.png'],
    'installable': True,
    'application': False,
   
}
