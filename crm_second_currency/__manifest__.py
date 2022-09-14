# -*- coding: utf-8 -*-
# Part of SysNeo. See LICENSE file for full copyright and licensing details.

{
    "name": "CRM Second Currency",
    'price': '0',
    'currency': "USD",
    "summary": "Adds a second currency to oportunity crm",
    'description': """
Second currency
===============
Adds a second currency to oportunity.
    """,
    "version": "13.0.1.0.0",
    "license": "Other proprietary",
    'category': 'Customer Relationship Management',
    "author": "SysNeo",
    "website": "https://sysneo.pe",
    "depends": ["base", "crm"],
    "data": [
        "views/crm_lead_view.xml",
    ],
    'images': ['images/crm_sc_00.png'],
    "demo": [],
    "installable": True,
}
