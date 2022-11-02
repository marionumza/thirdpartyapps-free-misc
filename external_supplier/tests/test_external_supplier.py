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

import logging
import xml.etree.ElementTree as ET
from datetime import date
from unittest.mock import patch, Mock, mock_open, call

import pysftp
import requests
import time
import markupsafe

from odoo.exceptions import UserError
from odoo.tests import common, tagged

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install')
class TestExternalSupplier(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Default external supplier'
        })
        self.external_supplier = self.env['external.supplier'].create({
            'name': 'Default',
            'supplier_id': self.supplier.id
        })
        self.product = self.env['product.product'].create({
            'name': 'Test product'
        })

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._compute_supplier_type_depending_values',
        autospec=True)
    def test_create(self, patched_compute):
        supp = self.env['external.supplier'].create({
            'name': 'Second',
            'supplier_id': self.env['res.partner'].create({'name': 'Default external supplier'}).id
        })
        self.assertIsNotNone(supp)
        patched_compute.assert_called_once_with(supp)

    # #################################
    # ACTIONS
    # #################################

    def test_action_check_number_thread(self):
        pass

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_sftp_connection',
           autospec=True)
    def test_action_check_ftp_success(self, patched_get_connection):
        res = self.external_supplier.action_check_ftp()
        patched_get_connection.assert_called_once_with(self.external_supplier)
        self.assertDictEqual(res, {
            'effect': {
                'fadeout': 'slow',
                'message': "SFTP connection is properly setup !",
                'img_url': '/web/static/src/img/smile.svg',
                'type': 'rainbow_man',
            }
        })

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_sftp_connection',
           autospec=True)
    def test_action_check_ftp_failures(self, patched_get_connection):
        patched_get_connection.side_effect = pysftp.SSHException()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_ftp()
        patched_get_connection.assert_called_once_with(self.external_supplier)

        patched_get_connection.reset_mock()
        patched_get_connection.side_effect = pysftp.AuthenticationException()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_ftp()
        patched_get_connection.assert_called_once_with(self.external_supplier)

        patched_get_connection.reset_mock()
        patched_get_connection.side_effect = Exception()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_ftp()
        patched_get_connection.assert_called_once_with(self.external_supplier)

    @patch('requests.head')
    def test_action_check_xml_success(self, patched_head):
        self.external_supplier.xml_server_url = 'https://blah.blu'
        res = self.external_supplier.action_check_xml()
        patched_head.assert_called_once_with('https://blah.blu')
        self.assertDictEqual(res, {
            'effect': {
                'fadeout': 'slow',
                'message': "HTTP(s) connection to XML server is properly setup !",
                'img_url': '/web/static/src/img/smile.svg',
                'type': 'rainbow_man',
            }
        })

    @patch('requests.head')
    def test_action_check_xml_failures(self, patched_head):
        self.external_supplier.xml_server_url = 'https://blah.blu'
        patched_head.side_effect = requests.exceptions.MissingSchema()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_xml()
        patched_head.assert_called_once_with('https://blah.blu')

        patched_head.reset_mock()
        patched_head.side_effect = requests.exceptions.ConnectionError()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_xml()
        patched_head.assert_called_once_with('https://blah.blu')

        patched_head.reset_mock()
        patched_head.side_effect = Exception()
        with self.assertRaises(UserError):
            with self.assertLogs(level='ERROR'):
                self.external_supplier.action_check_xml()
        patched_head.assert_called_once_with('https://blah.blu')

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._download_products_file',
           autospec=True)
    def test_action_download_products_file(self, patched_download):
        res = self.external_supplier.action_download_products_file()
        patched_download.assert_called_once_with(self.external_supplier)
        self.assertDictEqual(res, {
            'effect': {
                'fadeout': 'slow',
                'message': "Download succeed !",
                'img_url': '/web/static/src/img/smile.svg',
                'type': 'rainbow_man',
            }
        })
        self.assertIsNotNone(self.external_supplier.last_product_file_download_date)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products', autospec=True)
    def test_action_sync_products(self, patched_sync):
        self.external_supplier.action_sync_products()
        patched_sync.assert_called_once_with(self.external_supplier)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products', autospec=True)
    def test_action_sync_demo_products(self, patched_sync):
        self.external_supplier.action_sync_demo_products()
        patched_sync.assert_called_once_with(self.external_supplier, 10)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.action_download_products_file',
           autospec=True)
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier.action_sync_products',
           autospec=True)
    def test_cron_sync_products(self, patched_download, patched_sync):
        auto_supplier = self.env['external.supplier'].create({
            'name': 'AUTO',
            'supplier_id': self.env['res.partner'].create({'name': 'Auto Moto'}).id,
            'auto_sync_product': True,
        })
        self.env['external.supplier'].create({
            'name': 'MANUAL',
            'supplier_id': self.env['res.partner'].create({'name': 'Manual Sanchez'}).id,
            'auto_sync_product': False,
        })
        self.env['external.supplier'].cron_sync_products()
        patched_download.assert_called_once_with(auto_supplier)
        patched_sync.assert_called_once_with(auto_supplier)

    # #################################
    # PUBLIC
    # #################################

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_new_order_response_from_supplier',
        autospec=True)
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._handle_new_order_supplier_response',
        autospec=True)
    def test_send_order_to_external_supplier(self, patched_handle, patched_get):
        patched_get.return_value = "bla"
        self.external_supplier.send_order_to_external_supplier('fake purchase order')
        patched_get.assert_called_once_with(self.external_supplier, 'fake purchase order')
        patched_handle.assert_called_once_with(self.external_supplier, 'bla', 'fake purchase order')

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_from_external_supplier',
        autospec=True)
    def test_update_order_lines_price_and_stock_price_decrease(self, mock_get_pna):
        product = self.env['product.product'].create({
            'name': 'test',
            'standard_price': 10.0,
            'description': 'Description of test',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id
            })]
        })
        supplier_info = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': product.id,
            'product_code': 121545,
            'price': 10.0,
        })
        purchase_order = self.env['purchase.order'].create({
            'name': 'P00001',
            'partner_id': self.supplier.id,
            'order_date': '20210429',
            'order_line': [(0, 0, {
                'name': 'Average Ice Cream',
                'product_id': product.id,
                'product_qty': 1,
                'product_uom': product.uom_id.id,
                'price_unit': 10.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        mock_get_pna.return_value = 3.99, 6
        self.external_supplier.update_order_lines_price_and_stock(purchase_order.order_line)
        mock_get_pna.assert_called_once_with(self.external_supplier, purchase_order.order_line)
        self.assertEqual(purchase_order.order_line.price_and_stock_state, 'price_decreased')
        self.assertEqual(purchase_order.order_line.price_unit, 3.99)
        self.assertEqual(purchase_order.order_line.stock_supplier, '6')
        self.assertEqual(product.standard_price, 3.99)
        self.assertEqual(supplier_info.price, 3.99)

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_from_external_supplier',
        autospec=True)
    def test_update_order_lines_price_and_stock_price_increase(self, mock_get_pna):
        product = self.env['product.product'].create({
            'name': 'test',
            'standard_price': 10.0,
            'description': 'Description of test',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id
            })]
        })
        supplier_info = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': product.id,
            'product_code': 121545,
            'price': 10.0,
        })
        purchase_order = self.env['purchase.order'].create({
            'name': 'P00001',
            'partner_id': self.supplier.id,
            'order_date': '20210429',
            'order_line': [(0, 0, {
                'name': 'Average Ice Cream',
                'product_id': product.id,
                'product_qty': 1,
                'product_uom': product.uom_id.id,
                'price_unit': 10.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        mock_get_pna.return_value = 13.99, 6
        self.external_supplier.update_order_lines_price_and_stock(purchase_order.order_line)
        mock_get_pna.assert_called_once_with(self.external_supplier, purchase_order.order_line)
        self.assertEqual(purchase_order.order_line.price_and_stock_state, 'price_increased')
        self.assertEqual(purchase_order.order_line.price_unit, 13.99)
        self.assertEqual(purchase_order.order_line.stock_supplier, '6')
        self.assertEqual(product.standard_price, 13.99)
        self.assertEqual(supplier_info.price, 13.99)

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_from_external_supplier',
        autospec=True)
    def test_update_order_lines_price_and_stock_out_of_stock(self, mock_get_pna):
        product = self.env['product.product'].create({
            'name': 'test',
            'standard_price': 10.0,
            'description': 'Description of test',
            'seller_ids': [(0, 0, {
                'name': self.supplier.id
            })]
        })
        supplier_info = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': product.id,
            'product_code': 121545,
            'price': 10.0,
        })
        purchase_order = self.env['purchase.order'].create({
            'name': 'P00001',
            'partner_id': self.supplier.id,
            'order_date': '20210429',
            'order_line': [(0, 0, {
                'name': 'Average Ice Cream',
                'product_id': product.id,
                'product_qty': 2,
                'product_uom': product.uom_id.id,
                'price_unit': 10.0,
                'date_planned': time.strftime('%Y-%m-%d')
            })]
        })
        mock_get_pna.return_value = 13.99, 0
        self.external_supplier.update_order_lines_price_and_stock(purchase_order.order_line)
        mock_get_pna.assert_called_once_with(self.external_supplier, purchase_order.order_line)
        self.assertEqual(purchase_order.order_line.price_and_stock_state, 'out_of_stock')
        self.assertEqual(purchase_order.order_line.price_unit, 13.99)
        self.assertEqual(purchase_order.order_line.stock_supplier, '0')
        self.assertEqual(product.standard_price, 13.99)
        self.assertEqual(supplier_info.price, 13.99)

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._handle_external_supplier_order_status_response',
        autospec=True)
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_order_status_response',
           autospec=True)
    def test_get_order_status_from_external_supplier(self, patched_get, patched_handle):
        patched_get.return_value = "bla"
        self.external_supplier.get_order_status_from_external_supplier('fake stock picking')
        patched_get.assert_called_once_with(self.external_supplier, 'fake stock picking')
        patched_handle.assert_called_once_with(self.external_supplier, 'bla', 'fake stock picking')

    # #################################
    # PRIVATE
    # #################################

    # #################################
    # CONNECTION ESTABLISHMENT
    # #################################

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_connection_with_external_supplier_server',
        autospec=True)
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._send_request_through_supplier_connection',
        autospec=True)
    def test__send_request_to_supplier(self, patched_send, patched_create):
        patched_create.return_value = 'connection'
        with self.assertLogs(level='DEBUG'):
            self.external_supplier._send_request_to_supplier('fake endpoint', 'fake request')
            patched_create.assert_called_once_with(self.external_supplier)
            patched_send.assert_called_once_with(self.external_supplier, 'connection', 'fake endpoint', 'fake request')

    def test__send_request_through_supplier_connection(self):
        conn = Mock()
        conn.request = Mock()
        mock_response = Mock()
        mock_response.read = Mock(return_value="read result")
        conn.getresponse = Mock(return_value=mock_response)
        conn.close = Mock()
        res = self.external_supplier._send_request_through_supplier_connection(conn, 'endpoint', 'request')
        conn.request.assert_called_once_with("POST", 'endpoint', 'request')
        conn.getresponse.assert_called_once_with()
        mock_response.read.assert_called_once_with()
        conn.close.assert_called_once_with()
        self.assertEqual(res, 'read result')

    # #################################
    # DOWNLOAD PRODUCT FILE & CONNECTION TO SFTP METHODS
    # #################################

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_sftp_connection',
           autospec=True)
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._ensure_local_files_directory_exists',
        autospec=True)
    def test__download_products_file(self, patched_ensure_exists, patched_get_connection):
        patched_get_connection.return_value.__enter__.return_value.isfile = Mock(return_value=False)
        patched_get_connection.return_value.__enter__.return_value.get = Mock()
        self.external_supplier.write({
            'ftp_server_path': 'distant/bla',
            'products_filename': 'products.txt',
            'local_files_directory_path': 'local/bla',
        })
        with self.assertRaises(UserError):
            self.external_supplier._download_products_file()
        patched_ensure_exists.assert_called_once_with(self.external_supplier)
        patched_get_connection.assert_called_once_with(self.external_supplier)

        patched_get_connection.return_value.__enter__.return_value.isfile.return_value = True
        self.external_supplier._download_products_file()

        patched_get_connection.return_value.__enter__.return_value.get.side_effect = Exception()
        with self.assertRaises(UserError):
            with self.assertLogs(level="ERROR"):
                self.external_supplier._download_products_file()

    def test__get_sftp_connection(self):
        pass  # TODO complex to test

    @patch('os.path.exists')
    def test__ensure_local_files_directory_exists(self, patched_exists):
        self.external_supplier.local_files_directory_path = 'bla'
        patched_exists.return_value = False
        with self.assertRaises(UserError):
            self.external_supplier._ensure_local_files_directory_exists()
        patched_exists.assert_called_once_with('bla')

        patched_exists.reset_mock()
        patched_exists.return_value = True
        self.external_supplier._ensure_local_files_directory_exists()
        patched_exists.assert_called_once_with('bla')

    @patch('os.path.exists')
    def test__ensure_local_product_file_exists(self, patched_exists):
        self.external_supplier.write({
            'local_files_directory_path': 'bla',
            'products_filename': 'p.txt'
        })
        patched_exists.return_value = False
        with self.assertRaises(UserError):
            self.external_supplier._ensure_local_product_file_exists()
        patched_exists.assert_called_once_with('bla/p.txt')

        patched_exists.reset_mock()
        patched_exists.return_value = True
        self.external_supplier._ensure_local_product_file_exists()
        patched_exists.assert_called_once_with('bla/p.txt')

    # #################################
    # SYNC PRODUCTS PRIVATE METHODS
    # #################################

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_sync_product_thread',
           autospec=True)
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products_batch_multithread')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products_batch')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_csv_file_content')
    def test__sync_products_with_thread(self, patched_get, patched_sync, patched_sync_thread, patched_thread):
        csv_content = list(range(1004))
        self.external_supplier.thread_amount = 4
        patched_get.return_value = csv_content

        self.external_supplier._sync_products(19)
        patched_get.assert_called_once_with(19)
        patched_sync.assert_called_once_with(csv_content, [], [])
        patched_sync_thread.assert_not_called()
        patched_thread.assert_not_called()

        patched_get.reset_mock()
        patched_sync.reset_mock()
        self.external_supplier._sync_products()
        self.assertEqual(patched_thread.call_count, 4)
        patched_sync.assert_not_called()
        patched_sync_thread.assert_not_called()  # as we don't start threads
        patched_thread.assert_has_calls([
            call(self.external_supplier, 0, 251, csv_content),
            call(self.external_supplier, 1, 251, csv_content),
            call(self.external_supplier, 2, 251, csv_content),
            call(self.external_supplier, 3, 251, csv_content),
        ])

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_sync_product_thread',
           autospec=True)
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products_batch_multithread')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._sync_products_batch')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_csv_file_content')
    def test__sync_products_no_thread(self, patched_get, patched_sync, patched_create_thread, patched_sync_thread):
        csv_content = list(range(10))
        patched_get.return_value = csv_content

        self.external_supplier._sync_products()
        patched_get.assert_called_once_with(False)
        patched_sync.assert_called_once_with(csv_content, [], [])
        patched_create_thread.assert_not_called()
        patched_sync_thread.assert_not_called()

        patched_get.reset_mock()
        patched_sync.reset_mock()
        self.external_supplier._sync_products(19)
        patched_get.assert_called_once_with(19)
        patched_sync.assert_called_once_with(csv_content, [], [])
        patched_create_thread.assert_not_called()
        patched_sync_thread.assert_not_called()

    def test__sync_products_batch_multithread(self):
        pass  # TODO need to find a way to correctly test cursors

    def test__sync_products_batch(self):
        pass  # TODO

    def test__csv_row_to_product_values(self):
        self.external_supplier.write({
            'product_code_csv_header': 'aa code',
            'eanupc_csv_header': 'bb eanupc',
            'product_cost_csv_header': 'ii cost',
            'product_price_csv_header': 'cc price',
            'product_name_csv_header': 'dd name',
            'product_description_csv_header': 'ee desc',
            'manufacturer_csv_header': 'ff manu',
            'weight_csv_header': 'gg weight',
            'category_id_csv_header': 'hh categ',
        })
        csv_row = {
            'aa code': 'bla',
            'bb eanupc': '"b"',
            'cc price': '2,99',
            'dd name': 'd',
            'ee desc': 'e',
            'ff manu': 'abc,def',
            'gg weight': 'g',
            'hh categ': 'h',
            'ii cost': '1,99',
        }
        res = self.external_supplier._csv_row_to_product_values(csv_row)
        self.assertDictEqual(res, {
            'code': 'bla',
            'barcode': 'b',
            'cost': '1.99',
            'price': '2.99',
            'name': 'd',
            'description': 'e',
            'manufacturer': 'abc,def',
            'weight': 'g',
            'category_id': 'h',
        })

        self.external_supplier.product_description_csv_header = False
        res = self.external_supplier._csv_row_to_product_values(csv_row)
        self.assertDictEqual(res, {
            'code': 'bla',
            'barcode': 'b',
            'cost': '1.99',
            'price': '2.99',
            'name': 'd',
            'manufacturer': 'abc,def',
            'weight': 'g',
            'category_id': 'h',
        })

        self.external_supplier.manufacturer_csv_header = False
        res = self.external_supplier._csv_row_to_product_values(csv_row)
        self.assertDictEqual(res, {
            'code': 'bla',
            'barcode': 'b',
            'cost': '1.99',
            'price': '2.99',
            'name': 'd',
            'weight': 'g',
            'category_id': 'h',
        })

        self.external_supplier.weight_csv_header = False
        res = self.external_supplier._csv_row_to_product_values(csv_row)
        self.assertDictEqual(res, {
            'code': 'bla',
            'barcode': 'b',
            'cost': '1.99',
            'price': '2.99',
            'name': 'd',
            'category_id': 'h',
        })

        self.external_supplier.category_id_csv_header = False
        res = self.external_supplier._csv_row_to_product_values(csv_row)
        self.assertDictEqual(res, {
            'code': 'bla',
            'barcode': 'b',
            'cost': '1.99',
            'price': '2.99',
            'name': 'd'
        })

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._ensure_local_product_file_exists')
    @patch('builtins.open', mock_open(read_data='blu'))
    def test__open_csv_file(self, patched_ensure):
        self.external_supplier._open_csv_file()
        patched_ensure.assert_called_once_with()

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._open_csv_file')
    @patch('csv.DictReader')
    def test__get_csv_file_content(self, patched_dictreader, patched_open):
        fake_opened_file = mock_open(read_data='blu')
        patched_open.return_value.__enter__.return_value = fake_opened_file
        self.external_supplier.write({
            'csv_file_encoding': 'utf-8',
            'csv_file_delimiter': ',',
            'products_filename': 'products.zip',
            'local_files_directory_path': '/path/to/',
        })

        # just need for it to return an iterator
        def dict_reader_side_effect(file, delimiter, quotechar):
            for i in "blu":
                yield i

        patched_dictreader.side_effect = dict_reader_side_effect

        res = self.external_supplier._get_csv_file_content()
        patched_open.assert_called_once()
        patched_dictreader.assert_called_once_with(fake_opened_file, delimiter=",", quotechar='"')
        self.assertListEqual(res, ['b', 'l', 'u'])

        patched_open.reset_mock()
        patched_dictreader.reset_mock()
        res = self.external_supplier._get_csv_file_content(limit=2)
        patched_open.assert_called_once()
        patched_dictreader.assert_called_once_with(fake_opened_file, delimiter=",", quotechar='"')
        self.assertListEqual(res, ['b', 'l'])

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_product')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._update_product')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._search_product')
    def test__create_or_update_product(self, patched_search, patched_update, patched_create):
        product = self.env['product.product'].create({
            'name': 'BLA',
        })
        patched_search.return_value = product
        product_value = {'a': 'b'}
        purchase_taxes = [1]
        sales_taxes = [2]

        self.external_supplier._create_or_update_product(product_value, purchase_taxes, sales_taxes)
        patched_search.assert_called_once_with(product_value)
        patched_update.assert_called_once_with(product, product_value, purchase_taxes, sales_taxes)
        patched_create.assert_not_called()

        patched_search.reset_mock()
        patched_update.reset_mock()
        patched_search.return_value = self.env['product.product'].browse()

        self.external_supplier._create_or_update_product(product_value, purchase_taxes, sales_taxes)
        patched_search.assert_called_once_with(product_value)
        patched_create.assert_called_once_with(product_value, purchase_taxes, sales_taxes)
        patched_update.assert_not_called()

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_product_supplierinfo')
    def test__update_product(self, patched_create):
        category = self.env['product.category'].create({'name': 'Bla'})
        product = self.env['product.product'].create({
            'name': 'BLA',
            'standard_price': 12.50,
            'list_price': 15.00,
            'weight': 11.24,
            'description': 'BLA',
            'description_sale': 'BLA',
            'categ_id': category.id,
            'active': False,
            'manufacturer': 'Odoo',
        })
        suppinfo = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'min_qty': 0,
            'price': 12.50,
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_name': 'BLA',
            'product_id': product.id,
            'product_code': 'THISISTHEOLDCODE'
        })
        new_category = self.env['product.category'].create({'name': 'BLU NEW CAT'})
        sale_tax = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        purchase_tax = self.env['account.tax'].search([('type_tax_use', '=', 'purchase')])
        product_values = {
            'name': 'BLU NEW',
            'cost': 4000.54,
            'price': 5444.54,
            'code': 'THISISTHEOLDCODE',
            'manufacturer': 'BHC',
            'category_id': new_category.id,
            'weight': 750.59
        }
        self.external_supplier._update_product(product, product_values, purchase_tax.ids, sale_tax.ids)
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.product_tmpl_id)
        self.assertEqual(product.product_tmpl_id.name, 'BLU NEW')
        self.assertAlmostEqual(product.product_tmpl_id.list_price, 5444.54)
        self.assertAlmostEqual(product.product_tmpl_id.standard_price, 12.50,
                               msg="Standard price is not updated as it's computed from now on")
        self.assertAlmostEqual(product.product_tmpl_id.weight, 750.59)
        self.assertEqual(product.product_tmpl_id.description, markupsafe.Markup('<p>BLU NEW</p>'))
        self.assertEqual(product.product_tmpl_id.description_sale, 'BLU NEW')
        self.assertEqual(product.product_tmpl_id.categ_id, new_category)
        self.assertEqual(product.product_tmpl_id.last_synchro_supplier, date.today())
        self.assertEqual(product.taxes_id, sale_tax)
        self.assertEqual(product.supplier_taxes_id, purchase_tax)
        self.assertTrue(product.active)
        self.assertEqual(product.manufacturer, 'BHC')
        self.assertEqual(product.default_code, 'THISISTHEOLDCODE')
        self.assertAlmostEqual(product.price_extra, 0.0)
        self.assertAlmostEqual(suppinfo['price'], 4000.54)
        self.assertEqual(suppinfo.product_code, 'THISISTHEOLDCODE')
        self.assertEqual(suppinfo.product_id, product)
        patched_create.assert_not_called()

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_product_supplierinfo')
    def test__update_product_no_existing_suppinfo(self, patched_create):
        category = self.env['product.category'].create({'name': 'Bla'})
        product = self.env['product.product'].create({
            'name': 'BLA',
            'standard_price': 12.50,
            'list_price': 15.50,
            'weight': 11.24,
            'description': 'BLA',
            'description_sale': 'BLA',
            'categ_id': category.id,
            'active': False,
            'manufacturer': 'Odoo',
        })

        new_category = self.env['product.category'].create({'name': 'BLU NEW CAT'})
        sale_tax = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        purchase_tax = self.env['account.tax'].search([('type_tax_use', '=', 'purchase')])
        product_values = {
            'name': 'BLU NEW',
            'cost': 4000.54,
            'price': 5444.54,
            'code': 'NEWCODE',
            'manufacturer': 'BHC',
            'category_id': new_category.id,
            'weight': 750.59
        }
        self.external_supplier._update_product(product, product_values, purchase_tax.ids, sale_tax.ids)
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.product_tmpl_id)
        self.assertEqual(product.product_tmpl_id.name, 'BLU NEW')
        self.assertAlmostEqual(product.product_tmpl_id.standard_price, 12.50,
                               msg="Standard price is not updated as it's computed from now on")
        self.assertAlmostEqual(product.product_tmpl_id.list_price, 5444.54)
        self.assertAlmostEqual(product.product_tmpl_id.weight, 750.59)
        self.assertEqual(product.product_tmpl_id.description, markupsafe.Markup('<p>BLU NEW</p>'))
        self.assertEqual(product.product_tmpl_id.description_sale, 'BLU NEW')
        self.assertEqual(product.product_tmpl_id.categ_id, new_category)
        self.assertEqual(product.product_tmpl_id.last_synchro_supplier, date.today())
        self.assertEqual(product.taxes_id, sale_tax)
        self.assertEqual(product.supplier_taxes_id, purchase_tax)
        self.assertTrue(product.active)
        self.assertEqual(product.manufacturer, 'BHC')
        self.assertEqual(product.default_code, 'NEWCODE')
        self.assertAlmostEqual(product.price_extra, 0.0)
        patched_create.assert_called_once_with(product_values, product)

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_product_supplierinfo')
    def test__create_product(self, patched_create):
        self.external_supplier.default_category_id = self.env['product.category'].create({'name': 'DEFAULT BLUE'})
        product_category = self.env['product.category'].create({'name': 'Bla'})
        product_values = {
            'category_id': product_category.id,
            'name': 'BLU',
            'cost': 40.54,
            'price': 42.42,
            'manufacturer': 'BHC',
            'code': 'BLAH',
            'barcode': 'BLUCH',
            'weight': 10.42
        }
        sale_tax = self.env['account.tax'].create({
            'name': 'test tax 1',
            'amount': 0,
            'type_tax_use': 'sale'
        })
        purchase_tax = self.env['account.tax'].create({
            'name': 'test tax 1',
            'amount': 0,
            'type_tax_use': 'purchase'
        })
        sale_tax += sale_tax.copy()
        product = self.external_supplier._create_product(product_values, purchase_tax.ids, sale_tax.ids)
        patched_create.assert_called_once_with(product_values, product)
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.product_tmpl_id)
        self.assertEqual(product.product_tmpl_id.name, 'BLU')
        self.assertAlmostEqual(product.product_tmpl_id.list_price, 42.42)
        self.assertAlmostEqual(product.product_tmpl_id.standard_price, 40.54)
        self.assertAlmostEqual(product.product_tmpl_id.weight, 10.42)
        self.assertEqual(product.product_tmpl_id.description, markupsafe.Markup('<p>BLU</p>'))
        self.assertEqual(product.product_tmpl_id.description_sale, 'BLU')
        self.assertEqual(product.product_tmpl_id.categ_id, product_category)
        buy = self.env.ref('purchase_stock.route_warehouse0_buy')
        mto = self.env.ref('stock.route_warehouse0_mto')
        self.assertEqual(len(product.product_tmpl_id.route_ids), 2)
        self.assertIn(buy, product.product_tmpl_id.route_ids)
        self.assertIn(mto, product.product_tmpl_id.route_ids)
        self.assertTrue(product.product_tmpl_id.supplier)
        self.assertEqual(product.product_tmpl_id.type, 'product')
        self.assertEqual(product.product_tmpl_id.last_synchro_supplier, date.today())
        self.assertEqual(product.taxes_id, sale_tax)
        self.assertEqual(product.supplier_taxes_id, purchase_tax)
        self.assertTrue(product.active)
        self.assertEqual(product.manufacturer, 'BHC')
        self.assertEqual(product.default_code, 'BLAH')
        self.assertAlmostEqual(product.price_extra, 0.0)
        self.assertEqual(product.barcode, 'BLUCH')

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._create_product_supplierinfo')
    def test__create_product_no_taxes_no_weight(self, patched_create):
        self.external_supplier.default_category_id = self.env['product.category'].create({'name': 'Bla'})
        product_values = {
            'name': 'BLU',
            'cost': 40.54,
            'price': 42.42,
            'manufacturer': 'BHC',
            'code': 'BLAH',
            'barcode': 'BLUCH'
        }
        product = self.external_supplier._create_product(product_values, [], [])
        patched_create.assert_called_once_with(product_values, product)
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.product_tmpl_id)
        self.assertEqual(product.product_tmpl_id.name, 'BLU')
        self.assertAlmostEqual(product.product_tmpl_id.list_price, 42.42)
        self.assertAlmostEqual(product.product_tmpl_id.standard_price, 40.54)
        self.assertAlmostEqual(product.product_tmpl_id.weight, 0.0)
        self.assertEqual(product.product_tmpl_id.description, markupsafe.Markup('<p>BLU</p>'))
        self.assertEqual(product.product_tmpl_id.description_sale, 'BLU')
        self.assertEqual(product.product_tmpl_id.categ_id, self.external_supplier.default_category_id)
        buy = self.env.ref('purchase_stock.route_warehouse0_buy')
        mto = self.env.ref('stock.route_warehouse0_mto')
        self.assertEqual(len(product.product_tmpl_id.route_ids), 2)
        self.assertIn(buy, product.product_tmpl_id.route_ids)
        self.assertIn(mto, product.product_tmpl_id.route_ids)
        self.assertTrue(product.product_tmpl_id.supplier)
        self.assertEqual(product.product_tmpl_id.type, 'product')
        self.assertEqual(product.product_tmpl_id.last_synchro_supplier, date.today())
        self.assertEqual(len(product.taxes_id), 0)
        self.assertEqual(len(product.supplier_taxes_id), 0)
        self.assertTrue(product.active)
        self.assertEqual(product.manufacturer, 'BHC')
        self.assertEqual(product.default_code, 'BLAH')
        self.assertAlmostEqual(product.price_extra, 0.0)
        self.assertEqual(product.barcode, 'BLUCH')

    def test__create_product_supplierinfo(self):
        p = self.env['product.product'].create({
            'barcode': 'bla',
            'default_code': 'blu',
            'name': 'ble'
        })
        product_values = {
            'cost': 19.99,
            'price': 29.99,
            'name': 'BALA',
            'code': 'CODE'
        }
        suppinfo = self.external_supplier._create_product_supplierinfo(product_values, p)
        self.assertEqual(suppinfo.name, self.supplier)
        self.assertEqual(suppinfo.min_qty, 0)
        self.assertAlmostEqual(suppinfo.price, 19.99)
        self.assertEqual(suppinfo.product_tmpl_id, p.product_tmpl_id)
        self.assertEqual(suppinfo.product_name, 'BALA')
        self.assertEqual(suppinfo.product_code, 'CODE')
        self.assertEqual(suppinfo.product_id, p)

    def test__search_product(self):
        product_values = {
            'barcode': 'bla',
            'code': 'blu'
        }
        res = self.external_supplier._search_product(product_values)
        self.assertEqual(len(res), 0)
        p1 = self.env['product.product'].create({
            'barcode': 'bla',
            'default_code': 'blu',
            'name': 'ble'
        })
        res = self.external_supplier._search_product(product_values)
        self.assertEqual(res, p1)

        p1.action_archive()
        res = self.external_supplier._search_product(product_values)
        self.assertEqual(res, p1)

    # #################################
    # UPDATE PRICE AND STOCK PRIVATE METHODS
    # #################################

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._handle_price_and_stock_response')
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_response_from_supplier')
    def test__get_price_and_stock_from_external_supplier(self, patched_get, patched_handle):
        patched_get.return_value = 'response'
        self.external_supplier._get_price_and_stock_from_external_supplier('order line')
        patched_get.assert_called_once_with('order line')
        patched_handle.assert_called_once_with('order line', 'response')

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._send_request_to_supplier')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_endpoint')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_price_and_stock_request')
    def test__get_price_and_stock_response_from_supplier(self, patched_req, patched_end, patched_send):
        patched_req.return_value = 'request'
        patched_end.return_value = 'endpoint'
        patched_send.return_value = 'response'
        res = self.external_supplier._get_price_and_stock_response_from_supplier('order line')
        patched_req.assert_called_once_with('order line')
        patched_end.assert_called_once_with()
        patched_send.assert_called_once_with('endpoint', 'request')
        self.assertEqual(res, 'response')

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._extract_price_and_quantity')
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._ensure_no_error_for_price_and_quantity_response')
    @patch('xml.etree.ElementTree.fromstring')
    def test__handle_price_and_stock_response(self, patched_from_string, patched_ensure, patched_extract):
        pe = ET.ParseError()
        pe.code = 13
        patched_from_string.side_effect = pe

        with self.assertLogs(level='ERROR'):
            with self.assertRaises(UserError):
                self.external_supplier._handle_price_and_stock_response("order_line", "response")
        patched_ensure.assert_not_called()
        patched_extract.assert_not_called()

        patched_from_string.side_effect = None
        patched_from_string.return_value = "xml node"
        self.external_supplier._handle_price_and_stock_response("order_line", "response")
        patched_ensure.assert_called_once_with("order_line", "xml node")
        patched_extract.assert_called_once_with("xml node")

    # #################################
    # SEND NEW ORDER PRIVATE METHODS
    # #################################

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._send_request_to_supplier')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_create_order_endpoint')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_create_order_request')
    def test__get_new_order_response_from_supplier(self, patched_req, patched_end, patched_send):
        patched_req.return_value = 'request'
        patched_end.return_value = 'endpoint'
        patched_send.return_value = 'response'
        res = self.external_supplier._get_new_order_response_from_supplier('purchase order')
        patched_req.assert_called_once_with('purchase order')
        patched_end.assert_called_once_with()
        patched_send.assert_called_once_with('endpoint', 'request')
        self.assertEqual(res, 'response')

    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._handle_new_successful_order_response')
    @patch(
        'odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._ensure_no_error_for_order_response')
    @patch('xml.etree.ElementTree.fromstring')
    def test__handle_new_order_supplier_response(self, patched_from_string, patched_ensure, patched_handle):
        patched_from_string.side_effect = ET.ParseError()

        with self.assertRaises(UserError):
            self.external_supplier._handle_new_order_supplier_response("response", "purchase_order")
        patched_ensure.assert_not_called()
        patched_handle.assert_not_called()

        patched_from_string.side_effect = None
        patched_from_string.return_value = "xml node"
        self.external_supplier._handle_new_order_supplier_response("response", "purchase_order")
        patched_ensure.assert_called_once_with("xml node")
        patched_handle.assert_called_once_with("xml node", "purchase_order")

    # #################################
    # ORDER STATUS PRIVATE METHODS
    # #################################

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._send_request_to_supplier')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_order_status_endpoint')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._get_order_status_request')
    def test__get_order_status_response(self, patched_req, patched_end, patched_send):
        patched_req.return_value = 'request'
        patched_end.return_value = 'endpoint'
        patched_send.return_value = 'response'
        res = self.external_supplier._get_order_status_response('stock picking')
        patched_req.assert_called_once_with('stock picking')
        patched_end.assert_called_once_with()
        patched_send.assert_called_once_with('endpoint', 'request')
        self.assertEqual(res, 'response')

    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._extract_order_status')
    @patch('odoo.addons.external_supplier.models.external_supplier.ExternalSupplier._ensure_no_error_for_order_status')
    @patch('xml.etree.ElementTree.fromstring')
    def test__handle_external_supplier_order_status_response(self, patched_from_string, patched_ensure,
                                                             patched_extract):
        patched_from_string.side_effect = ET.ParseError()
        patched_extract.return_value = ("2012-12-12", "success")
        stock_picking = Mock(handle_status_update=Mock(return_value=None), write=Mock())

        with self.assertRaises(UserError):
            self.external_supplier._handle_external_supplier_order_status_response("response", stock_picking)
        patched_ensure.assert_not_called()
        patched_extract.assert_not_called()

        patched_from_string.side_effect = None
        patched_from_string.return_value = "xml node"
        self.external_supplier._handle_external_supplier_order_status_response("response", stock_picking)
        patched_ensure.assert_called_once_with("xml node")
        patched_extract.assert_called_once_with("xml node", stock_picking)
        stock_picking.handle_status_update.assert_called_once_with("2012-12-12", "success")
        stock_picking.write.assert_not_called()

        stock_picking.handle_status_update.reset_mock()
        fake_history_command = Mock(id=42)
        stock_picking.handle_status_update.return_value = fake_history_command
        self.external_supplier._handle_external_supplier_order_status_response("response", stock_picking)
        stock_picking.handle_status_update.assert_called_once_with("2012-12-12", "success")
        stock_picking.write.assert_called_once_with({'history_line': [(4, 42)]})

    # #################################
    # UTILS METHODS
    # #################################

    def test__get_supplierinfo(self):
        product = self.env['product.product'].create({
            'name': 'Yo'
        })

        with self.assertRaises(UserError):
            self.external_supplier._get_supplierinfo(product)
        found_suppinfo = self.external_supplier._get_supplierinfo(product, raise_if_not_found=False)
        self.assertEqual(found_suppinfo, self.env['product.supplierinfo'].browse())

        suppinfo = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_id': product.id
        })
        with self.assertRaises(UserError):
            self.external_supplier._get_supplierinfo(product)
        found_suppinfo = self.external_supplier._get_supplierinfo(product, raise_if_not_found=False)
        self.assertEqual(found_suppinfo, suppinfo)

    def test__get_supplierinfo_through_tpl(self):
        product = self.env['product.product'].create({
            'name': 'Yo'
        })
        suppinfo = self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_tmpl_id': product.product_tmpl_id.id
        })
        with self.assertRaises(UserError):
            self.external_supplier._get_supplierinfo(product)

        suppinfo.product_code = 'HOY'
        found_suppinfo = self.external_supplier._get_supplierinfo(product)
        self.assertEqual(found_suppinfo, suppinfo)
