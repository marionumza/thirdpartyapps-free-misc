######################################################################################################
#
# Copyright © B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# This code is subject to the BHC License Agreement
# Please see the License.txt file for more information
# All other rights reserved
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
######################################################################################################

{
    'name': 'External supplier',
    'version': '1.0',
    'depends': ['base', 'purchase', 'sale', 'product', 'stock', 'web', 'account', 'purchase_stock'],
    'author': 'BHC',
    'category': 'Generic Modules/Others',
    "description": """
    This module provides an XML integration between Odoo and external supplier. 
    It allows to maintain the supplier product catalog and price list up to date automatically. 
    It also provides a real-time integration for quotation, sales, purchases and deliveries. 
    Actions in Odoo generate requests toward supplier to get information, or to place an order directly, 
    without using any external tool or website. 

    """,
    "data": [
        'security/security.xml',
        'data/cron_data.xml',
        'views/product_product_view.xml',
        'views/supplier_config_view.xml',
        'views/sale_order_view.xml',
        'views/stock_view.xml',
        'views/purchase_order_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo_xml': [],
    'external_dependencies': {'python': ['pysftp']},
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
