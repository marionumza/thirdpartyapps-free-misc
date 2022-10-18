# -*- coding: utf-8 -*-
#    Copyright (C) 2007  pronexo.com  (https://www.pronexo.com)
#    All Rights Reserved.
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
############################################################################## # 
# 
{
    'name': "POS - Cliente Tipo de Responsabilidad AFIP - Odoo Argentina",

    'summary': """
        Adds Identification type field and AFIP Responsability type field to pos customer view.
    """,

    'description': """
        Adds Identification type field and AFIP Responsability type field to pos customer view.
    """,

    'author': "Pronexo",
    'website': "https://www.pronexo.com",

    'category': 'Sales/Point of Sale',
    'version': '15.0.1.3',
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'USD',
    
    'depends': ['point_of_sale', 'l10n_latam_base','contacts'],

    'assets': {
        'point_of_sale.assets': [
            'pos_l10n_ar_identification/static/src/js/models.js',
            'pos_l10n_ar_identification/static/src/js/screens.js',
        ],
        'web.assets_qweb': [
            'pos_l10n_ar_identification/static/src/xml/**/*',
        ],
    }, 
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
