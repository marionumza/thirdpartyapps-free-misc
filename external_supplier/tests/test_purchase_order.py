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

import time
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestPurchaseOrder(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.partner'].create({'name': "Dummy Supplier"})
        self.external_supplier = self.env['external.supplier'].create({
            'name': 'test',
            'supplier_id': self.supplier.id
        })
        self.product = self.env['product.product'].create({
            'name': 'test',
            'price': 10,
            'description': 'Description of test',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id
            })]
        })
        self.supplier_info = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': self.product.id
        })

    @patch('odoo.addons.external_supplier.models.purchase_order.PurchaseOrder._send_to_supplier')
    def test_button_confirm_no_external_supplier(self, patched_send):
        # Only need to test that _send_to_supplier() is called when it has to
        po = self.env['purchase.order'].create({
            'partner_id': '1',
            'name': 'P00001'
        })
        po.button_confirm()
        patched_send.assert_not_called()
        self.assertNotIn(po.state, ('draft', 'sent'))

    @patch('odoo.addons.external_supplier.models.purchase_order.PurchaseOrder._send_to_supplier')
    def test_button_confirm_with_external_supplier(self, patched_send):
        # Only need to test that _send_to_supplier() is called when it has to
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        po.button_confirm()
        patched_send.assert_called_once_with()
        self.assertNotIn(po.state, ('draft', 'sent'))

    @patch('odoo.addons.external_supplier.models.purchase_order.PurchaseOrder._send_to_supplier')
    def test_button_confirm_with_external_supplier_no_auto_send(self, patched_send):
        # Only need to test that _send_to_supplier() is called when it has to
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'send_automatically_to_supplier': False,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        po.button_confirm()
        patched_send.assert_not_called()
        self.assertNotIn(po.state, ('draft', 'sent'))

    @patch('odoo.addons.external_supplier.models.purchase_order.PurchaseOrder._send_to_supplier')
    def test_button_confirm_with_external_supplier_error(self, patched_send):
        # Only need to test that _send_to_supplier() is called when it has to
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        initial_state = po.state
        patched_send.side_effect = UserError("Hey")
        with self.assertRaises(UserError):
            po.button_confirm()
        patched_send.assert_called_once_with()
        self.assertEqual(po.state, initial_state)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.update_order_lines_price_and_stock')
    def test_action_sync_price_and_stock(self, patched_update):
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        po.action_sync_price_and_stock()
        patched_update.assert_called_once_with(po.order_line)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.update_order_lines_price_and_stock')
    def test_action_sync_price_and_stock_no_ext_supp(self, patched_update):
        po = self.env['purchase.order'].create({
            'partner_id': 1,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        with self.assertRaises(UserError):
            po.action_sync_price_and_stock()
        patched_update.assert_not_called()

    @patch('odoo.addons.external_supplier.models.purchase_order.PurchaseOrder._notify_order_sent_to_external_supplier')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.send_order_to_external_supplier')
    def test__send_to_supplier(self, patched_send, patched_notify):
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 60.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        po._send_to_supplier()
        patched_send.assert_called_once_with(po)
        patched_notify.assert_called_once_with()

    @patch('odoo.addons.mail.models.mail_thread.MailThread.message_post')
    def test__notify_order_sent_to_external_supplier(self, patched_post):
        po = self.env['purchase.order'].create({
            'partner_id': '1',
            'name': 'P00001'
        })
        po._notify_order_sent_to_external_supplier()
        patched_post.assert_called_once()
