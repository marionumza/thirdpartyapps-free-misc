# -*- coding: utf-8 -*-
#################################################################################
# Author      : Trend for econtent. (<https://www.trend-is.co/>)
# Copyright(c): 2016-Present Trend for econtent.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': "Contacts Validation",
    'summary': "This App From Trend Company to Validate Fields in Contacts",
    'description': """
        This module will Validate Those Fields with Option to stop it from Settings: \n
            1- Validate Mobile, Phone.\n
            2- Validate Email.\n
            3- Validate Tax ID, Company register.\n
     """,
    'author': "Trend for e-content",
    'website': "https://www.trend-is.co/",
    'category': 'Contacts',
    'depends': ['base_setup'],
    'license': 'LGPL-3',
    'version': '1.0',
    'data': [
        'views/res_config_setting_view.xml',
        'views/res_partner_view.xml',
    ],
    'images': ['static/description/banner.gif'],
}
