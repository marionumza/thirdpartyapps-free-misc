# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Botspot Infoware Pvt. Ltd. <www.botspotinfoware.com>
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
    'name': "Repair Parts Immediate Buying",
    'author': 'Botspot Infoware Pvt. Ltd.',
    'category': 'Manufacturing',
    'summary': """Repair parts immediate buying for buying quickly and easily""",
    'website': 'https://www.botspotinfoware.com',
    'company': 'Botspot Infoware Pvt. Ltd.',
    'maintainer': 'Botspot Infoware Pvt. Ltd.',
    'description': """Repair Parts Immediate Buying for buying quickly and easily using puchase part button""",
    'version': '1.0',
    'depends': ['base', 'repair', 'purchase'],
    'data': [
               "views/purchase_views.xml",
               "views/repair_order_view.xml",
            ],

    "images":  ['static/description/Repair Parts Immediate Buying.gif'],
    "qweb":  [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
