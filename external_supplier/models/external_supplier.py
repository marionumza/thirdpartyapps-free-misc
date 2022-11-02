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

import csv
import itertools
import logging
import math
import os
import os.path
import threading
import time
import traceback
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from datetime import datetime
from queue import Queue

import pysftp
import requests

from odoo import api, fields, models, registry, _
from odoo.exceptions import UserError
from odoo.tools import float_compare

MINIMUM_AMOUNT_TO_USE_THREADS = 1000

_logger = logging.getLogger(__name__)


# FIXME add a button here to easily re-enable MTO route ?

class ExternalSupplier(models.Model):
    _name = "external.supplier"
    _description = "External Supplier"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_name(self):
        if self.supplier_type:
            return '{}{}'.format(self.supplier_type[0].upper(), self.supplier_type[1:].lower())
        return ''

    def _get_default_xml_server_url(self):
        return ''

    def _get_default_ftp_server_url(self):
        return ''

    def _get_default_ftp_server_path(self):
        return ''

    def _get_default_local_files_directory_path(self):
        return ''

    def _get_default_products_filename(self):
        return ''

    def _get_default_product_code_csv_header(self):
        return ''

    def _get_default_eanupc_csv_header(self):
        return ''

    def _get_default_manufacturer_csv_header(self):
        return ''

    def _get_default_weight_csv_header(self):
        return ''

    def _get_default_category_id_csv_header(self):
        return ''

    def _get_default_product_cost_csv_header(self):
        return ''

    def _get_default_product_price_csv_header(self):
        return ''

    def _get_default_product_name_csv_header(self):
        return ''

    def _get_default_product_description_csv_header(self):
        return ''

    name = fields.Char(string="Name", help="Name associated with the configuration", required=True)
    supplier_type = fields.Selection([])
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)

    xml_server_url = fields.Char(string='XML server address')
    xml_server_login = fields.Char(string='XML server login')
    xml_server_password = fields.Char(string='XML server password')

    ftp_server_url = fields.Char(string='FTP server address')
    ftp_server_login = fields.Char(string='FTP server login')
    ftp_server_password = fields.Char(string='FTP server password')
    ftp_server_path = fields.Char(string="FTP server files path")

    products_filename = fields.Char(string='Products file name')
    local_files_directory_path = fields.Char(string="Local path for downloaded CSV files")
    auto_sync_product = fields.Boolean(string="Automatically sync products", default=False)
    last_sync_date = fields.Datetime(string='Products synced at', readonly=True)
    last_product_file_download_date = fields.Datetime(string='Product file downloaded at', readonly=True)
    synced_products_amount = fields.Integer(compute='_compute_synced_data')
    synced_categories_amount = fields.Integer(compute='_compute_synced_data')
    synced_product_ids = fields.Many2many('product.product', compute='_compute_synced_data')
    synced_category_ids = fields.Many2many('product.category', compute='_compute_synced_data')

    default_category_id = fields.Many2one('product.category', string='Default product category')
    sales_taxes = fields.Many2many('account.tax', "supplier_sales_taxes", 'supplier_sales', "sales_tax",
                                   string='Sales taxes', domain=[('type_tax_use', '=', 'sale')])
    purchase_taxes = fields.Many2many('account.tax', "supplier_purchase_taxes", 'supplier_purchase', "purchase_tax",
                                      string='Purchases taxes', domain=[('type_tax_use', '=', 'purchase')])
    thread_amount = fields.Integer(string='Amount of threads to use', default=1)

    # Configuration file
    csv_file_encoding = fields.Selection([('utf-8', 'UTF-8'), ('iso-8859-1', 'ISO-8859-1')], string="CSV file encoding",
                                         default='utf-8', required=True)
    csv_file_delimiter = fields.Selection([(',', ',')], string="CSV file delimiter", default=',', required=True)
    csv_file_quotechar = fields.Selection([('"', '"'), ('|', '|')], string="CSV file quotechar", default='"',
                                          required=True)

    # Configuration product file
    product_code_csv_header = fields.Char("Product Code column identifier")
    eanupc_csv_header = fields.Char("EANUPC Code column identifier")
    manufacturer_csv_header = fields.Char("Product manufacturer name column identifier")
    weight_csv_header = fields.Char("Weight column identifier")
    category_id_csv_header = fields.Char("Product category id column identifier")
    product_cost_csv_header = fields.Char("Product Cost column identifier")
    product_price_csv_header = fields.Char("Product Price column identifier")
    product_name_csv_header = fields.Char("Product Name column identifier")
    product_description_csv_header = fields.Char("Product Description column identifier")

    @api.onchange('supplier_type')
    def _compute_supplier_type_depending_values(self):
        fields = [
            'name',
            'xml_server_url',
            'ftp_server_url',
            'ftp_server_path',
            'local_files_directory_path',
            'products_filename',
            'product_code_csv_header',
            'eanupc_csv_header',
            'manufacturer_csv_header',
            'weight_csv_header',
            'category_id_csv_header',
            'product_cost_csv_header',
            'product_price_csv_header',
            'product_name_csv_header',
            'product_description_csv_header',
        ]
        for record in self:
            write_data = {}
            for field in fields:
                if not getattr(record, field):
                    write_data[field] = getattr(record, '_get_default_{}'.format(field))()
            if write_data:
                record.write(write_data)

    def _compute_synced_data(self):
        for record in self:
            record.synced_category_ids = self.env['product.category'].search([
                ('id', 'child_of', record.default_category_id.id)
            ]).ids
            record.synced_product_ids = self.env['product.supplierinfo'].sudo().search([
                ('name', '=', record.supplier_id.id),
                ('product_id.categ_id', 'in', record.synced_category_ids.ids)
            ]).mapped('product_id.id')
            record.synced_categories_amount = len(record.synced_category_ids)
            record.synced_products_amount = len(record.synced_product_ids)

    @api.model
    def create(self, vals_list):
        """ OVERRIDE """
        records = super().create(vals_list)
        records._compute_supplier_type_depending_values()
        return records

    # #################################
    # ACTIONS
    # #################################

    # not tested
    def action_check_number_thread(self):
        """
        FIXME this method should be clarified.
        Check and determine the amount of thread the system can support.
        """
        thread_count = 1
        flag = False
        while flag == False:
            i = 0
            tab_thread = []
            my_queue = Queue()
            while i <= thread_count:
                threaded_sending = threading.Thread(target=lambda q, arg1: q.put(self._test_function(False)),
                                                    args=(my_queue, False))
                res = threaded_sending.start()
                tab_thread.append(threaded_sending)
                i += 1
            _logger.info(thread_count)
            if not res:
                for thread in tab_thread:
                    while thread.isAlive():
                        try:
                            thread.join()
                        except Exception as e:
                            flag = True
                            break
                while not my_queue.empty():
                    if my_queue.get():
                        flag = True
                        break
                if flag == False:
                    thread_count += 1
                else:
                    _logger.info("Final thread")
                    _logger.info(len(tab_thread))
                    self.thread_amount = int(len(tab_thread) / 4)
                    break
            else:
                break

    def action_check_ftp(self):
        """
        Try to connect to FTP in order to check connection information.
        """
        self.ensure_one()
        try:
            with self._get_sftp_connection():
                pass
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': _("SFTP connection is properly setup !"),
                    'img_url': '/web/static/src/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        except pysftp.SSHException as e:
            _logger.exception(e)
            raise UserError(_("SFTP connection failed, please check the server URL address."))
        except pysftp.AuthenticationException as e:
            _logger.exception(e)
            raise UserError(_("Authentication failed, please check your credentials."))
        except Exception as e:
            _logger.exception(e)
            raise UserError(_("Connection error. Check the connection information."))

    def action_check_xml(self):
        """
        Try to connect to XML server in order to check connection information.
        """
        self.ensure_one()
        try:
            requests.head(self.xml_server_url)
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': _("HTTP(s) connection to XML server is properly setup !"),
                    'img_url': '/web/static/src/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        except requests.exceptions.MissingSchema as e:
            _logger.exception(e)
            raise UserError(_("Connection to XML server failed, please check that URL starts with 'http(s)://' !"))
        except requests.exceptions.ConnectionError as e:
            _logger.exception(e)
            raise UserError(_("Connection to XML server failed, please check that URL is correct !"))
        except Exception as e:
            _logger.exception(e)
            raise UserError(_("Connection error. Check the connection information."))

    def action_download_products_file(self):
        """
        Download the product file.
        """
        self.ensure_one()
        _logger.info(_('Downloading products file...'))
        self._download_products_file()
        _logger.info(_('Products file downloaded'))
        self.last_product_file_download_date = datetime.now()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Download succeed !',
                'img_url': '/web/static/src/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

    def action_view_synced_categories(self):
        self.ensure_one()
        action = self.env.ref('product.product_category_action_form').read()[0]
        action['domain'] = [('id', 'in', self.synced_category_ids.ids)]
        return action

    def action_view_synced_products(self):
        self.ensure_one()
        action = self.env.ref('stock.product_template_action_product').read()[0]
        action['domain'] = [('id', 'in', self.synced_product_ids.mapped('product_tmpl_id.id'))]
        return action

    def action_sync_products(self):
        """
        Read products from downloaded file and synchronize them with products in database.
        """
        self.ensure_one()
        self._sync_products()

    def action_sync_demo_products(self):
        """
        Read some products from downloaded file and synchronize them with products in database.
        """
        self.ensure_one()
        self._sync_products(10)

    @api.model
    def cron_sync_products(self):
        """
        Auto-synchronize all external suppliers with auto_sync_product flag set to true.
        """
        suppliers = self.env['external.supplier'].search([('auto_sync_product', '=', True)])
        for supplier in suppliers:
            try:
                supplier.action_download_products_file()
                supplier.action_sync_products()
            except Exception as e:
                supplier._handle_exception(e)

    # #################################
    # PUBLIC
    # #################################

    def send_order_to_external_supplier(self, purchase_order):
        """
        Takes care of sending the confirmed purchase order to the external supplier.
        :param purchase_order: the purchase order to be sent. This method is called in purchase_order confirm process.
        :type purchase_order: purchase.order
        """
        response = self._get_new_order_response_from_supplier(purchase_order)
        self._handle_new_order_supplier_response(response, purchase_order)

    def update_order_lines_price_and_stock(self, order_lines):
        """
        Update sale (resp purchase) order lines price and stock by performing an online check to external supplier.
        :param order_lines: the order lines to consider
        :type order_lines: purchase.order.line's or sale.order.line's
        """
        self.ensure_one()
        # FIXME should be possible to make all in only one HTTP request
        for order_line in order_lines:
            new_price, quantity = self._get_price_and_stock_from_external_supplier(order_line)
            line_qty = order_line.product_qty if hasattr(order_line, 'product_qty') else order_line.product_uom_qty
            standard_price = order_line.product_id.standard_price
            if float_compare(standard_price, new_price, precision_digits=2) != 0:
                # Price has changed, we update it in supplier info
                supplier_info_ids = self._get_supplierinfo(order_line.product_id)
                supplier_info_ids.write({'price': new_price})
            if line_qty and line_qty > quantity:
                price_and_stock_state = 'out_of_stock'
            else:
                if standard_price > new_price:
                    price_and_stock_state = 'price_decreased'
                else:
                    price_and_stock_state = 'price_increased'
            order_line.write({
                'price_and_stock_state': price_and_stock_state,
                'price_unit': new_price,
                'stock_supplier': quantity
            })
            order_line.product_id.standard_price = new_price
        order_lines.mapped('order_id').message_post(
            body=_("Prices and stocks have been synchronized with external supplier."))

    def get_order_status_from_external_supplier(self, stock_picking):
        """
        Takes care of asking status for a given order to supplier.
        This method is called by the button "Status' on stock picking form view.
        :param stock_picking:
        :type stock_picking: stock.picking
        """
        response = self._get_order_status_response(stock_picking)
        return self._handle_external_supplier_order_status_response(response, stock_picking)

    # #################################
    # PRIVATE
    # #################################

    # #################################
    # CONNECTION ESTABLISHMENT
    # #################################

    # Should be overridden if not using connection objects
    def _send_request_to_supplier(self, endpoint, request):
        """
        Send a request to the external supplier.
        :param endpoint: the endpoint to contact
        :param request: the request to send
        :return: the response received from the supplier
        """
        _logger.debug('→ Sending following request to %s' % endpoint)
        _logger.debug(request)
        conn = self._create_connection_with_external_supplier_server()
        return self._send_request_through_supplier_connection(conn, endpoint, request)

    # Should be overridden if using connection objects
    def _create_connection_with_external_supplier_server(self):
        """
        Create a connection object with the external supplier server.
        :rtype: (http.client.HTTPSConnection|http.client.HTTPConnection)
        """
        pass

    def _send_request_through_supplier_connection(self, conn, endpoint, request):
        """
        Send a request to a given endpoint to a given connection.
        :param conn: the connection object
        :type conn: http.client.HTTPSConnection|http.client.HTTPConnection
        :param endpoint: the endpoint as a string
        :type endpoint: str
        :param request: the request as a string (XML generally)
        :type request: str
        :return: http.client.HTTPResponse
        """
        conn.request("POST", endpoint, request)
        response = conn.getresponse()
        response = response.read()
        _logger.debug('← Received response below')
        _logger.debug(response)
        conn.close()
        return response

    # #################################
    # DOWNLOAD PRODUCT FILE & CONNECTION TO SFTP METHODS
    # #################################

    def _download_products_file(self):
        """
        Download product file through parametrized sftp connection.
        """
        self.ensure_one()
        self._ensure_local_files_directory_exists()
        distant_path = os.path.join(self.ftp_server_path, self.products_filename)
        local_path = os.path.join(self.local_files_directory_path, self.products_filename)
        with self._get_sftp_connection() as sftp:
            if not sftp.isfile(distant_path):
                raise UserError(_("Products file ('%s') not found on FTP server !") % distant_path)
            try:
                sftp.get(distant_path, local_path)
                _logger.info('Product file downloaded and stored at "{}"'.format(local_path))
            except Exception as e:
                _logger.exception(e)
                raise UserError(_('An error occurred while downloading product file !'))

    # FIXME name could be too specific as here it may be ftp not sftp
    @contextmanager
    def _get_sftp_connection(self):
        """
        Get a sftp connection to the configured server.
        :return: a pysftp.Connection object if all went well, raise errors if not.
        :rtype: pysftp.Connection
        """
        _logger.debug('Trying connection {}@{}'.format(self.ftp_server_login, self.ftp_server_url))
        cnopts = pysftp.CnOpts()
        hostkeys = None
        if cnopts.hostkeys.lookup(self.ftp_server_url) == None:
            _logger.debug('New host, will add host key')
            hostkeys = cnopts.hostkeys
            # And do not verify host key of the new host
            cnopts.hostkeys = None

        with pysftp.Connection(host=self.ftp_server_url, username=self.ftp_server_login,
                               password=self.ftp_server_password, cnopts=cnopts) as connection:
            if hostkeys != None:
                _logger.debug('Connected to new host, storing its hostkey')
                hostkeys.add(self.ftp_server_url, connection.remote_server_key.get_name(), connection.remote_server_key)
                hostkeys.save(pysftp.helpers.known_hosts())
            yield connection

    def _ensure_local_files_directory_exists(self):
        """
        Make sure local path to store downloaded files exists.
        """
        if not os.path.exists(self.local_files_directory_path):
            raise UserError(
                _("Local directory '%s' does not exist, please provide a valid one !")
                % os.path.abspath(self.local_files_directory_path))

    def _ensure_local_product_file_exists(self):
        """
        Make sure product file has been downloaded and exist locally.
        """
        local_path = os.path.join(self.local_files_directory_path, self.products_filename)
        if not os.path.exists(local_path):
            raise UserError(
                _("Local product file '%s' not found, download it first !")
                % os.path.abspath(local_path))

    # #################################
    # SYNC PRODUCTS PRIVATE METHODS
    # #################################

    def _sync_products(self, limit=False):
        """
        Synchronize products with downloaded file. Multi-thread this treatment if there is a lot to sync.
        :param limit: the limit to read from downloaded file.
        :type limit: int
        """
        purchase_taxes_ids = self.purchase_taxes.ids
        sales_taxes_ids = self.sales_taxes.ids
        _logger.info('Products synchronization started')
        if not self.thread_amount:
            self.thread_amount = 1
        product_csv_lines = self._get_csv_file_content(limit)
        number_row = len(product_csv_lines)
        if limit:
            number_row = limit
        if number_row >= MINIMUM_AMOUNT_TO_USE_THREADS and self.thread_amount > 1:
            cluster_size = math.ceil(number_row / self.thread_amount)
            thread_list = [
                self._create_sync_product_thread(i, cluster_size, product_csv_lines)
                for i in range(self.thread_amount)
            ]
            for thread in thread_list:
                thread.join()
        else:
            self._sync_products_batch(product_csv_lines, purchase_taxes_ids, sales_taxes_ids)
        self.last_sync_date = datetime.now()
        _logger.info('Products synchronization ended')
        return True

    def _create_sync_product_thread(self, thread_index, cluster_size, csv_lines):
        """
        Create a thread responsible to read some lines from CSV and sync them with products in database.
        :param thread_index: the index of the thread in all those created in order to determine which products this
        thread should handle
        :type thread_index: int
        :param cluster_size: the size the clusters to make (ex : 4 threads to handle 1000 lines, cluster_size should be 250)
        :type cluster_size: int
        :param csv_lines: all the lines from csv to be treated (all, even those that this thread won't handle)
        :type csv_lines: list
        :return: the created thread
        :rtype: threading.Thread
        """
        index_from = thread_index * cluster_size
        index_to = (thread_index + 1) * cluster_size
        product_file_lines = csv_lines[index_from:index_to]
        thread = threading.Thread(target=self._sync_products_batch_multithread,
                                  args=(product_file_lines, self.purchase_taxes.ids
                                        , self.sales_taxes.ids))
        thread.start()
        return thread

    def _sync_products_batch_multithread(self, product_file_lines, purchase_taxes, sales_taxes):
        """
        Creates a dict and sends to method create_or_update_product
        :param product_file_lines: tab contains dict
        :param purchase_taxes: tab
        :param sales_taxes: tab
        :return: call method create or update
        """
        # need to create an environment and a new cursor as it is executed in a separated thread
        new_cr = self.pool.cursor()
        alt_self = self.with_env(self.env(cr=new_cr)).sudo()
        try:
            i = 0
            for row in product_file_lines:
                _logger.debug(f'Handling row {i}/{len(product_file_lines)}')
                product_values = alt_self._csv_row_to_product_values(row)
                alt_self._create_or_update_product(product_values, purchase_taxes, sales_taxes)
                new_cr.commit()
                i += 1
        except Exception as e:
            raise
        finally:
            new_cr.close()

    def _sync_products_batch(self, product_file_lines, purchase_taxes, sales_taxes):
        """
        Creates a dict and sends to method create_or_update_product
        :param product_file_lines: tab contains dict
        :param purchase_taxes: tab
        :param sales_taxes: tab
        :return: call method create or update
        """
        i = 1
        for row in product_file_lines:
            _logger.debug(f'Handling row {i}/{len(product_file_lines)}')
            product_values = self._csv_row_to_product_values(row)
            if product_values:
                self._create_or_update_product(product_values, purchase_taxes, sales_taxes)
            i += 1

    def _csv_row_to_product_values(self, csv_row):
        """
        Transform the csv row to "normalize" product values, and transform some of them (like price if the price is
        written with a comma instead of a dot).
        :param csv_row: the csv row to transform
        :type csv_row: dict
        :return: the normalized product values
        :rtype: dict
        """
        cost = self._get_csv_value_or_fail(csv_row, self.product_cost_csv_header)
        price = self._get_csv_value_or_fail(csv_row, self.product_price_csv_header)
        product_values = {
            'code': self._get_csv_value_or_fail(csv_row, self.product_code_csv_header),
            'barcode': self._get_csv_value_or_fail(csv_row, self.eanupc_csv_header),
            'cost': cost.replace(',', '.') if cost else cost,
            'price': price.replace(',', '.') if price else price,
            'name': self._get_csv_value_or_fail(csv_row, self.product_name_csv_header),
        }
        if not product_values['name']:
            _logger.warning("Found a product without name, please be sure the right CSV column separator is selected !")
            _logger.warning(csv_row)
            return None
        if self.product_description_csv_header:
            product_values['description'] = csv_row[self.product_description_csv_header]
        if self.manufacturer_csv_header:
            product_values['manufacturer'] = csv_row[self.manufacturer_csv_header]
        if self.weight_csv_header:
            product_values['weight'] = csv_row[self.weight_csv_header]
        if self.category_id_csv_header:
            product_values['category_id'] = csv_row[self.category_id_csv_header]
        return {key: product_values[key].strip("'\" ") if product_values[key] else product_values[key]
                for key in product_values}

    def _get_csv_value_or_fail(self, csv_row, header):
        """
        Get a CSV value in a row or raise an error if value isn't present.
        :param csv_row: the csv row
        :type csv_row: dict
        :param header: the header name
        :type header: string
        :return: the value if found
        :rtype: str
        :raise: UserError if not found
        """
        value = csv_row.get(header)
        if value is None:
            _logger.error('Error occured while processing following csv row (%s header not found)' % header)
            _logger.error(csv_row)
            raise UserError(_(
                "'%s' header not found in CSV file, please be sure CSV file formatting and CSV file headers are well configured !") % header)
        return value

    def _open_csv_file(self):
        """
        Open the CSV file containing products information.
        :return file: the opened file handler
        :rtype: IO
        """
        file_path = os.path.join(self.local_files_directory_path, self.products_filename)
        self._ensure_local_product_file_exists()
        _logger.debug('Opening CSV file "{}" [{}]'.format(file_path, self.csv_file_encoding))
        return open(file_path, 'r', encoding=self.csv_file_encoding)

    def _get_csv_file_content(self, limit=False):
        """
        Get product CSV file content using DictReader.
        :param limit: the amount of line to read
        :type limit: integer
        :return: a list of rows contained in the csv file and stored as dict with headers as keys.
        :rtype: list
        """
        self.ensure_one()
        with self._open_csv_file() as file:
            _logger.debug('Parsing CSV file with {} as delimiter and {} as quotechar'.format(self.csv_file_delimiter,
                                                                                             self.csv_file_quotechar))
            reader = csv.DictReader(file, delimiter=self.csv_file_delimiter, quotechar=self.csv_file_quotechar)
            if not limit:
                return list(reader)
            else:
                return list(itertools.islice(reader, limit))

    def _create_or_update_product(self, product_values, purchase_tax_ids, sale_tax_ids):
        """
        Create or update the product based on given product values
        :param product_values: the product values
        :type product_values: dict
        :param purchase_tax_ids: the taxes to apply when purchasing this product
        :type purchase_tax_ids: list
        :param sale_tax_ids: the taxes to apply when this product is sold
        :type sale_tax_ids: list
        """
        supplier_product = self._search_product(product_values)
        if supplier_product:
            _logger.debug(f"Updating product \"{supplier_product.name}\" (#{supplier_product.id}) ...")
            self._update_product(supplier_product, product_values, purchase_tax_ids, sale_tax_ids)
        else:
            _logger.debug(f"Creating product \"{product_values['name']}'']\"...")
            self._create_product(product_values, purchase_tax_ids, sale_tax_ids)

    def _update_product(self, product, product_values, purchase_tax_ids, sale_tax_ids):
        """
        Update a product based on given product values.
        :param product: the product to update
        :type product: product.product
        :param product_values: the product values
        :type product_values: dict
        :param purchase_tax_ids: the taxes to apply when purchasing this product
        :type purchase_tax_ids: list
        :param sale_tax_ids: the taxes to apply when this product is sold
        :type sale_tax_ids: list
        """
        product_category_id = product_values.get('category_id', self.default_category_id.id)
        product_weight = product_values.get('weight', '0.0')
        product.product_tmpl_id.write({
            'name': product_values['name'],
            'standard_price': product_values['cost'],
            'list_price': product_values['price'],
            'weight': product_weight,
            'description': product_values['name'],
            'description_sale': product_values['name'],
            'categ_id': product_category_id,
            'active': True,
            'last_synchro_supplier': time.strftime("%Y-%m-%d")
        })

        supplier_info = self._get_supplierinfo(product, raise_if_not_found=False)
        if not supplier_info:
            self._create_product_supplierinfo(product_values, product)
        else:
            supplier_info.write({
                'price': float(product_values['cost']),
                'product_id': product.id,
                'product_tmpl_id': product.product_tmpl_id
            })

        product.write({
            'taxes_id': [(6, 0, sale_tax_ids)],
            'supplier_taxes_id': [(6, 0, purchase_tax_ids)],
            'default_code': product.default_code or product_values['code'],
            'active': True,
            'manufacturer': product_values['manufacturer']
        })

    def _create_product(self, product_values, purchase_tax_ids, sale_tax_ids):
        """
        Create a product based on given product values.
        :param product_values: the product values
        :type product_values: dict
        :param purchase_tax_ids: the taxes to apply when purchasing this product
        :type purchase_tax_ids: list
        :param sale_tax_ids: the taxes to apply when this product is sold
        :type sale_tax_ids: list
        """
        product_category_id = product_values.get('category_id', self.default_category_id.id)
        product_weight = product_values.get('weight', '0.0')
        buy_type = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        mto_type = self.env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        mto_type.active = True  # in v14 it's not active by default
        route_ids = []
        if buy_type:
            route_ids.append(buy_type.id)
        if mto_type:
            route_ids.append(mto_type.id)
        product_tmpl_id = self.env['product.template'].create({
            'name': product_values['name'],
            'standard_price': product_values['cost'],
            'list_price': product_values['price'],
            'weight': product_weight,
            'description': product_values['name'],
            'description_sale': product_values['name'],
            'categ_id': product_category_id,
            'route_ids': [(6, 0, route_ids)],
            'supplier': True,
            'type': 'product',
            'last_synchro_supplier': time.strftime("%Y-%m-%d")
        })
        product = self.env['product.product'].search([('product_tmpl_id', '=', product_tmpl_id.id)])
        self._create_product_supplierinfo(product_values, product)

        product_write = {
            'taxes_id': [(6, 0, sale_tax_ids)],
            'supplier_taxes_id': [(6, 0, purchase_tax_ids)],
            'active': True,
            'manufacturer': product_values['manufacturer'],
            'default_code': product_values['code'],
            'price_extra': 0.00,
        }
        if product_values['barcode']:
            product_write['barcode'] = product_values['barcode']
        product.write(product_write)
        return product

    def _create_product_supplierinfo(self, product_values, product):
        """
        Create product supplier info based on product_values and given product.
        :param product_values: the product values
        :type product_values: dict
        :param product: the product to update
        :type product: product.product
        :return: the created supplier info
        :rtype: product.supplierinfo
        """
        return self.env['product.supplierinfo'].create({
            'name': self.supplier_id.id,
            'min_qty': 0,
            'price': product_values['cost'],
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_name': product_values['name'],
            'product_id': product.id,
            'product_code': product_values['code']
        })

    def _search_product(self, product_values):
        """
        Search product based on product values coming from external supplier.
        :type product_values: dict
        :return: the found product
        :rtype: product.product
        """
        domain = [
            '|',
            ('barcode', '=', product_values['barcode']),
            ('default_code', '=', product_values['code'])
        ]
        product = self.env['product.product'].search(domain, limit=1)
        if product:
            return product
        return self.env['product.product'].with_context(active_test=False).search(domain)

    # #################################
    # UPDATE PRICE AND STOCK PRIVATE METHODS
    # #################################

    def _get_price_and_stock_from_external_supplier(self, order_line):
        """
        Takes care of asking price and stock information for a product to supplier.
        This method is called by the button "Synchronize price and stock from supplier" on sale.order and purchase.order
        form view.
        :param order_line: the order line with the product from which the price and stock information is needed.
        :type order_line: purchase.order.line or sale.order.line.
        :return: a tuple containing the price and the stock from the supplier regarding the product linked to the given
        order line
        :rtype: (float, int)
        """
        response = self._get_price_and_stock_response_from_supplier(order_line)
        return self._handle_price_and_stock_response(order_line, response)

    def _get_price_and_stock_response_from_supplier(self, order_line):
        """
        Create & send request to supplier based on a order line and get price and stock response
        for assigned product to order line.
        :param order_line: the order line
        :type order_line: purchase.order.line|sale.order.line
        :return: the response
        :rtype: http.client.HTTPResponse
        """
        endpoint = self._get_price_and_stock_endpoint()
        request = self._get_price_and_stock_request(order_line)
        return self._send_request_to_supplier(endpoint, request)

    def _handle_price_and_stock_response(self, order_line, response):
        """
        Handle a PnA response for a given order line
        :param order_line: the order line
        :type order_line: purchase.order.line|sale.order.line
        :param response: the response received from supplier server
        :type response: str
        :return: a tuple containing the price and the stock from the supplier regarding the product linked to the given
        order line
        :rtype: (float, int)
        """
        try:
            xml_root_node = ET.fromstring(response)
            self._ensure_no_error_for_price_and_quantity_response(order_line, xml_root_node)
            return self._extract_price_and_quantity(xml_root_node)
        except ET.ParseError as e:
            # parsing failed due to unregistered namespace prefixes
            # can happen with SOAP-ENV and default ns, we remove them and retry
            # TODO maybe use a better way here (like regex or parser)
            _logger.exception(e)
            if e.code == 27:
                try:
                    xml_root_node = ET.fromstring(response.replace('SOAP-ENV:', '').replace('ns:', ''))
                    self._ensure_no_error_for_price_and_quantity_response(order_line, xml_root_node)
                    return self._extract_price_and_quantity(xml_root_node)
                except ET.ParseError:
                    _logger.exception(e)
                    raise UserError(
                        _("Received response is not well formatted, please check logs or contact administrator"))
            raise UserError(
                _("Received response is not well formatted, please check logs or contact administrator"))

    # Should be overridden
    def _get_price_and_stock_endpoint(self):
        """
        Get the price and stock (PnA) endpoint to contact.
        :return: the PnA endpoint path
        :rtype: str
        """
        pass

    # Should be overridden
    def _get_price_and_stock_request(self, order_line):
        """
        Get the price and stock (PnA) request to send for given order line.
        :param order_line: the order line
        :type order_line: sale.order.line
        :return: the PnA request
        :rtype: str
        """
        pass

    # Should be overridden
    def _extract_price_and_quantity(self, xml_root_node):
        """
        Extract the price and the quantity from a given XML root node.
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        :return: the price and the quantity
        :rtype: (float, int)
        """
        pass

    # Should be overridden
    def _ensure_no_error_for_price_and_quantity_response(self, order_line, xml_root_node):
        """
        Ensure no error has been received as a response from external supplier when sending PnA request.
        This method is expected to raise an error if something wrong is detected in response.
        :param order_line: the order line concerned by the initial request
        :type order_line: sale.order.line
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        """
        pass

    # #################################
    # SEND NEW ORDER PRIVATE METHODS
    # #################################

    def _get_new_order_response_from_supplier(self, purchase_order):
        """
        Send new order request to supplier for given purchase order and return the response.
        :param purchase_order: the purchase order to send
        :type purchase_order: purchase.order
        :return: the response
        :rtype: http.client.HTTPResponse
        """
        request = self._get_create_order_request(purchase_order)
        endpoint = self._get_create_order_endpoint()
        return self._send_request_to_supplier(endpoint, request)

    def _handle_new_order_supplier_response(self, response, purchase_order):
        """
        Handle new order response received from supplier server
        :param response: the received response
        :type response: str
        :param purchase_order: the purchase order that has been sent to supplier
        :type purchase_order: purchase.order
        """
        try:
            xml_root_node = ET.fromstring(response)
        except ET.ParseError:
            raise UserError(_("Received response is not well formatted, please check logs or contact administrator"))
        self._ensure_no_error_for_order_response(xml_root_node)
        self._handle_new_successful_order_response(xml_root_node, purchase_order)

    # Should be overridden
    def _get_create_order_endpoint(self):
        """
        Get the create order endpoint to contact.
        :return: the create order endpoint path
        :rtype: str
        """
        pass

    # Should be overridden
    def _get_create_order_request(self, purchase_order):
        """
        Get the create order request to send for given purchase order.
        :param purchase_order: the purchase order
        :type purchase_order: purchase.order
        :return: the create order request
        :rtype: str
        """
        pass

    # Should be overridden
    def _ensure_no_error_for_order_response(self, xml_root_node):
        """
        Ensure no error has been received as a response from external supplier when sending create order request.
        This method is expected to raise an error if something wrong is detected in response.
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        """
        pass

    # Should be overridden
    def _handle_new_successful_order_response(self, xml_root_node, purchase_order):
        """
        Handle a successful order create response.
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        :param purchase_order: the purchase order
        :type purchase_order: purchase.order
        """
        pass

    # #################################
    # ORDER STATUS PRIVATE METHODS
    # #################################

    def _get_order_status_response(self, stock_picking):
        """
        Send order status request to supplier for given stock picking and return the response.
        :param stock_picking: the stock picking
        :type stock_picking: stock.picking
        :return: the response
        :rtype: http.client.HTTPResponse
        """
        request = self._get_order_status_request(stock_picking)
        endpoint = self._get_order_status_endpoint()
        return self._send_request_to_supplier(endpoint, request)

    def _handle_external_supplier_order_status_response(self, response, stock_picking):
        """
        Handle order status response received from supplier server
        :param response: the received response
        :type response: str
        :param stock_picking: the stock picking concerned by the order status
        :type stock_picking: stock.picking
        """
        try:
            xml_root_node = ET.fromstring(response)
        except ET.ParseError:
            raise UserError(_("Received response is not well formatted, please check logs or contact administrator"))
        self._ensure_no_error_for_order_status(xml_root_node)
        date, status = self._extract_order_status(xml_root_node, stock_picking)
        history_command = stock_picking.handle_status_update(date, status)
        if history_command:
            stock_picking.write({'history_line': [(4, history_command.id)]})

    # Should be overridden
    def _get_order_status_endpoint(self):
        """
        Get the order status endpoint to contact.
        :return: the order status endpoint path
        :rtype: str
        """
        pass

    # Should be overridden
    def _get_order_status_request(self, stock_picking):
        """
        Get the order status request to send for given stock picking.
        :param stock_picking: the stock picking
        :type stock_picking: stock.picking
        :return: the order status request
        :rtype: str
        """
        pass

    # Should be overridden
    def _ensure_no_error_for_order_status(self, xml_root_node):
        """
        Ensure no error has been received as a response from external supplier when sending order status request.
        This method is expected to raise an error if something wrong is detected in response.
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        """
        pass

    # Should be overridden
    def _extract_order_status(self, xml_root_node, stock_picking):
        """
        Extract the order status from a given XML root node.
        :param xml_root_node: the response XML root node
        :type xml_root_node: xml.etree.ElementTree.Element
        :return: date and status of the order, as a tuple
        :rtype: (str, str)
        """
        pass

    # #################################
    # UTILS METHODS
    # #################################

    def _get_supplierinfo(self, product, raise_if_not_found=True):
        """
        Get the supplierinfo for given product and supplier linked to current external supplier.
        :param product: the product
        :type product: product.product
        :param raise_if_not_found: True if method is expected to raise an exception if supplier info is not found, False
        otherwise
        :return: the found supplier info
        :rtype: product.supplierinfo
        """
        self.ensure_one()
        supplier_info = self.env['product.supplierinfo'].sudo().search([
            ('name', '=', self.supplier_id.id),
            ('product_id', '=', product.id)
        ], limit=1)
        if not supplier_info:
            supplier_info = self.env['product.supplierinfo'].sudo().search([
                ('name', '=', self.supplier_id.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
            ], limit=1)
        if raise_if_not_found:
            if not supplier_info:
                raise UserError(
                    _('The product "%s" cannot be supplied by selected supplier.') % product.name)
            if not supplier_info.product_code:
                raise UserError(
                    _('The product "%s" has no vendor reference for selected supplier.') % product.name)
        return supplier_info

    def _test_function(self, value):
        #  FIXME this method should be clarified.
        try:
            new_cr = self.pool.cursor()
            cr = registry(self._cr.dbname).cursor()
            self.with_env(self.env(cr=cr))
            time.sleep(0.5)
            cr.commit()
            cr.close()
            new_cr.close()
            return 0
        except Exception as e:
            return 1

    def _handle_exception(self, e):
        """
        Handle exception so that it's printed in the chatter.
        :param e: the exception
        """
        _logger.exception(e)
        e_str = traceback.format_exc()
        generic_msg = _(
            "An exception occurred during automatic synchronization to external supplier, please check logs.")
        body_html = f'''{generic_msg}<br /><br />
                        <pre>${e_str}</pre>
                        '''
        self.message_post(body=body_html, subtype_xmlid='mail.mt_comment')
