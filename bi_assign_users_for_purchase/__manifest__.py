# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "User Assignment For Purchase Order Based On State",
    "version" : "15.0.0.0",
    "category" : "Purchase",
    'license': 'OPL-1',
    'summary': 'User Assignment For Purchase Order Based On State, assignes to the user.',
    "description": """
    
   User Assignment For Purchase Order Based On State,assignes purchase order according
    user assign for po state
    user assign for po stage
    assign user for purchase stage
    user for purchase order stage
    
    to the set configuration 
    
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 000,
    "currency": 'EUR',
    "depends" : ['base','purchase'],
    "data": [
        'views/purchase_inherit_views.xml',
        'views/purchase_config_views.xml',
        'edi/assign_user_data.xml',
    ],
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/Sq1nJt4Pdyk',
    "images":["static/description/Banner.png"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
