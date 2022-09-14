###############################################################################
#
#    Flash Software, S.L.
#    Copyright (C) 2020-Flash Software, S.L. <www.flashodoo.com>
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
###############################################################################
{
    'name': 'Portal Hide Promotional Link',
    'summary': 'Hide Odoo promotional link in website sale orders and bottom right link',
    'category': 'Website',
    'version': '13.0.1.0.1',
    'author': 'FlashOdoo',
    'website': 'https://www.flashodoo.com',
    'license': 'AGPL-3',
    'depends': ['portal'],
    'data': [
        'views/portal_template.xml'
    ],
	'images': [
        'static/description/banner.png'
    ],
    'installable': True,
}
