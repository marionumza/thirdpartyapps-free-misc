# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt ltd'<www.botspotinfoware.com>
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
    'name': "Driver's Vehicle History",
    'author': 'Botspot infoware Pvt. Ltd.',
    'category': 'Fleet',
    'summary': """Used for gathering all vehicles details of the drivers. When a driver takes a deal for a vehicle then the start/end date is displayed on the driver's profile.""",
    'website': 'https://www.botspotinfoware.com',
    'company': 'Botspot Infoware Pvt. Ltd.',
    'maintainer': 'Botspot Infoware Pvt. Ltd.',
    'description': """Used for gathering all vehicles details of the drivers. When a driver takes a deal for a vehicle then the start/end date is displayed on the driver's profile.""",
    'versio': '1.0',
    'depends': ['base', 'fleet', 'sale'],
    'data': [
             "security/ir.model.access.csv",
             "views/vehicle_history_view.xml",
            ],
    "images":  ['static/description/Driver Vehical History.gif'],
    "qweb":  [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
