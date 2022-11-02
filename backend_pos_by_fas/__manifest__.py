# -*- coding: utf-8 -*-
###################################################################################
#
#    Muhammed Fasil - fasilwdr@hotmail.com
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{

     'name': "Backend POS",
     'author': "Fasil",
     'version': '0.1',
     'sequence': -1,
     'website': 'https://www.facebook.com/fasilwdr/',
     'license': 'LGPL-3',
     'summary': """
             Create POS Orders from Backend""",
     'description': """
             
         """,
     'depends': ['base','point_of_sale'],
     'data': [
         'views/pos_config.xml',
         'views/pos_session.xml',
         'views/pos_order.xml',
         'views/views.xml',
         'views/menu_actions.xml',
     ],
    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'],

}
