# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-TODAY NCoding Solutions
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
{
    'name': "Employee First Name, Middle Name & Last Name",
    'summary': """
       Employee,Partner and User Name in Full Format""",
    'description': """
        This module will give an option for expand Employee,Partner and User Name as First Name, Middle Name, Last Name
    """,
    'author': "NCoding Solutions",
    'license' : 'AGPL-3',
    'website': "http://www.ncodingsolutions.com",
    'category': 'Employee',
    'version': '0.1',
    'images': ['static/description/banner.png'],
    # any module necessary for this one to work correctly
    'depends': ['base','hr'],
    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
