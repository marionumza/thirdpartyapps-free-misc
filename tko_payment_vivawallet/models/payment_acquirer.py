# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hashlib
import base64
import requests
import json
from odoo import api, fields, models

Demo_URL = "https://demo-accounts.vivapayments.com"
Production_URL = "https://www.vivapayments.com"
class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('vivawallet', "PayUmoney")], ondelete={'vivawallet': 'set default'})
    vivawallet_client_id = fields.Char(
        string="Client ID",
        required_if_provider='vivawallet')
    vivawallet_client_secret = fields.Char(
        string="Cient Secret", required_if_provider='vivawallet', groups='base.group_system')
    vivawallet_source_code = fields.Char('Source Code')

    def get_vivawallet_url(self):
        if  self.state != 'test':
            URL = Production_URL
        else:
            URL = Demo_URL
        return URL

    @api.model
    def _get_compatible_acquirers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist PayUmoney acquirers when the currency is not INR. """
        acquirers = super()._get_compatible_acquirers(*args, currency_id=currency_id, **kwargs)

        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name != 'INR':
            acquirers = acquirers.filtered(lambda a: a.provider != 'vivawallet')

        return acquirers

    def _vivawallet_generate_token(self):
        """ Generate Token to communicate with VivaWallet API.
        """
        accesss_token = ''
        ## [cient_id]:[client_secret]
        client_id_scret_str = "%s:%s"%(self.vivawallet_client_id,self.vivawallet_client_secret)
        client_id_scret_bytes = client_id_scret_str.encode('ascii')
        client_id_scret_base64_bytes = base64.b64encode(client_id_scret_bytes)
        base64_client_id_scret = client_id_scret_base64_bytes.decode('ascii')
        headers = {
            'Authorization': 'Basic %s' % base64_client_id_scret,
        }

        data = {
            'grant_type': 'client_credentials',
        }
        URL = self.get_vivawallet_url()
        response = requests.post('%s/connect/token'%URL, headers=headers, data=data, timeout=5)
        print ("00000000000000000000000000000000000000000",response.text)
        accesss_token = json.loads(response.text).get('access_token')
        return accesss_token

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'vivawallet':
            return super()._get_default_payment_method_id()
        return self.env.ref('tko_payment_vivawallet.payment_method_vivawallet').id
