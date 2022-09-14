# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
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
    'name': "Location Condition",
    'author': 'Ascetic Business Solution',
    'category': 'Warehouse',
    'summary': """Location Condition""",
    'license': 'AGPL-3',
    'website': 'http://www.asceticbs.com',
    'description': """
""",
    'version': '13.0.1.0',
    'depends': ['base','stock'],
    'data': ['security/ir.model.access.csv','data/location_condition_data.xml','views/location_condition_view.xml','views/stock_location_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
