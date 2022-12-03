# -*- coding: utf-8 -*-

{
    'name': 'Generic Read Only User Access',
    "author": "Edge Technologies",
    'version': '15.0.1.0',
    'summary': "Read Only Access to User Limited Access Rights to User User Limited Access Read Only User Access User Read Only Access User Restricted Access Restriction On User Access Read Only User Read Only Access Login User Read Only Access Limited Portal User Access",
    'description': """ This App Provides A Functionality to Make Generic User Access Read Only for A Particular Login User Set User Read Only
    Restriction On User Level. Stop User Access from the System. User Restriction User Read Only Restriction. Restricated User Access. Limited User Access Limited. Security Restriction On User Level. User Security Restriction.

limited access rights to user
user limited access
read only user access
user read only access
user restricted access
restriction on user access
read only user
user read only access
login user read only access
login user limited access
login user restricted access
user access restriction 
login user access restriction
user security access restriction
user security restriction
customer read only access
supplier read only access
vendor read only access
limited customer access

    """,
    "license" : "OPL-1",
    'live_test_url': "https://youtu.be/J2k28TUCbZo",
    "images":['static/description/main_screenshot.png'],
    'depends': ['base','sale_management'],
    'data': [
            'security/user_read_only_group.xml',
            'security/ir.model.access.csv',
            'views/res_user_read_only.xml',
            ],
    'installable': True,
    'auto_install': False,
    'category': 'Extra Tools',
}
