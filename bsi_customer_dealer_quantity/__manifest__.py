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
    'name': "Customer's Dealers Quantity",
    'author': 'Botspot Infoware Pvt. Ltd.',
    'category': 'Sales',
    'summary': """When the dealer ordered a specific product quantity and if it's above the company's pre-defined criteria then A company can allow some special price to the dealer.""",
    'website': 'https://www.botspotinfoware.com',
    'company': 'Botspot Infoware Pvt. Ltd.',
    'maintainer': 'Botspot Infoware Pvt. Ltd.',
    'description': """When the dealer ordered a specific product quantity and if it's above the company's pre-defined criteria then A company can allow some special price to the dealer.""",
    'version': '1.0',
    'depends': ['base', 'sale'],
    'data': [
             "views/product_product_view.xml",
             "views/sale_view.xml",
             "views/res_partner_view.xml",
            ],
    "images":  ['static/description/Customer Dealers Quantity.gif'],
    "qweb":  [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
