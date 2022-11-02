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

from datetime import date
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestStockPicking(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.supplier = self.env['res.partner'].create({'name': "Dummy Supplier"})
        self.external_supplier = self.env['external.supplier'].create({
            'name': 'test',
            'supplier_id': self.supplier.id
        })

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.get_order_status_from_external_supplier')
    def test_action_update_status(self, patched_get):
        stock_picking = self.env['stock.picking'].create({
            'name': 'test_no_origin',
            'location_id': self.env['stock.location'].search([], limit=1).id,
            'location_dest_id': self.env['stock.location'].search([], limit=1, order='id desc').id,
            'picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
        })
        with self.assertRaises(UserError):
            stock_picking.action_update_status()
        stock_picking.partner_id = self.supplier.id
        with self.assertRaises(UserError):
            stock_picking.action_update_status()
        stock_picking.origin = 'POBLABLA'
        stock_picking.action_update_status()
        patched_get.assert_called_once_with(stock_picking)

    def test_handle_status_update(self):
        stock_picking = self.env['stock.picking'].create({
            'name': 'test_no_origin',
            'location_id': self.env['stock.location'].search([], limit=1).id,
            'location_dest_id': self.env['stock.location'].search([], limit=1, order='id desc').id,
            'picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
            'partner_id': self.supplier.id
        })
        exp_date = date(2021, 1, 1)
        amount_of_history_line_before = len(stock_picking.history_line)
        order_history = stock_picking.handle_status_update(exp_date, "Your packet is on its way")
        self.assertEqual(order_history.stock_picking_id, stock_picking)
        self.assertEqual(order_history.description, "Your packet is on its way")
        self.assertEqual(order_history.expected_date, exp_date)
        self.assertEqual(order_history.update_date, date.today())
        self.assertEqual(amount_of_history_line_before + 1, len(stock_picking.history_line))

        new_exp_date = date(2021, 2, 2)
        order_history = stock_picking.handle_status_update(new_exp_date, "Your packet is on its way")
        self.assertEqual(order_history.stock_picking_id, stock_picking)
        self.assertEqual(order_history.description, "Your packet is on its way")
        self.assertEqual(order_history.expected_date, new_exp_date)
        self.assertEqual(order_history.update_date, date.today())
        self.assertEqual(amount_of_history_line_before + 1, len(stock_picking.history_line))


@tagged('post_install', '-at_install')
class TestStockRule(common.TransactionCase):
    def test__run_buy(self):
        pass  # TODO complex to test
