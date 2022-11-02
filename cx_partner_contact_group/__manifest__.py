###################################################################################
# 
#    Copyright (C) Cetmix OÜ
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

{
    "name": "Odoo Advanced Partner Groups Contact Groups Contact Categories",
    "version": "15.0.1.0.0",
    "summary": """Powerful tool for managing Odoo Contact Partner Groups""",
    "author": "Ivan Sokolov, Cetmix",
    "category": "Sales",
    "license": "LGPL-3",
    "website": "https://cetmix.com",
    "description": """
Powerful tool for managing Contact Categories Odoo Partner Tags Groups
""",
    "depends": ["contacts"],
    "live_test_url": "https://demo.cetmix.com",
    "images": ["static/description/banner.png"],
    "data": [
        "views/partner_category.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cx_partner_contact_group/static/src/js/*.js",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
