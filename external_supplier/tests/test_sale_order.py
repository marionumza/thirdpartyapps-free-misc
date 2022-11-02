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

from unittest.mock import patch

import time

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestSaleOrder(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.partner'].create({'name': "Dummy Supplier"})
        self.product = self.env['product.product'].create({
            'name': 'test',
            'price': 10.0,
            'description': 'Description of test',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id
            })]
        })
        self.external_supplier = self.env['external.supplier'].create({
            'name': 'test',
            'supplier_id': self.supplier.id
        })
        self.supplier_info = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': self.product.id
        })

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.update_order_lines_price_and_stock')
    def test_action_sync_price_and_stock(self, patched_update):
        so = self.env['sale.order'].create({
            'partner_id': self.supplier.id,
            'order_line': [(0, 0, {
                'name': 'External Average Ice Cream',
                'external_supplier_id': self.external_supplier.id,
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'stock_supplier': 10
            }), (0, 0, {
                'name': 'Average Ice Cream',
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
            })]
        })
        so.action_sync_price_and_stock()
        patched_update.assert_called_once_with(so.order_line[0])

    @patch('odoo.addons.sale.models.sale_order.SaleOrder._action_confirm')
    def test_action_confirm(self, patched__confirm):
        pass  # TODO find a way to check the altered context
