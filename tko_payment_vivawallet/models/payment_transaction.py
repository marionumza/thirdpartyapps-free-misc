# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.exceptions import UserError
from odoo.addons.tko_payment_vivawallet.controllers.main import VivaWalletController
import requests
import json

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def vivawallet_smart_checkout(self):
        vivawallet_payment_acquirer = self.env.ref('tko_payment_vivawallet.payment_payment_acquirer_vivawallet')
        URL = vivawallet_payment_acquirer.get_vivawallet_url()
        access_token = vivawallet_payment_acquirer._vivawallet_generate_token()
        item_description = 'Charging........change me.!!!'

        headers = {
            'Authorization': 'Bearer %s' % access_token,
        }

        json_data = {
            'amount': self.amount,
            'customerTrns': item_description,
            'customer': {
                'email': self.partner_id.email,
                'fullName': self.partner_id.name,
                'phone': self.partner_id.phone,
                'countryCode': self.partner_id.country_id.code or 'GB',
                'requestLang': 'en-GB',
            },
            'paymentTimeout': 300,
            'preauth': False,
            'allowRecurring': False,
            'maxInstallments': 1,
            'paymentNotification': True,
            'tipAmount': 1,
            'disableExactAmount': False,
            'disableCash': True,
            'disableWallet': True,
            'sourceCode': vivawallet_payment_acquirer.vivawallet_source_code,
            'merchantTrns': item_description,
            'tags': [
                self.partner_id.name,
                self.reference,
            ],
        }

        response = requests.post('https://demo-api.vivapayments.com/checkout/v2/orders', headers=headers,
                                 json=json_data)
        orderCode = json.loads(response.text).get('orderCode')
        if orderCode:
            self.acquirer_reference = orderCode
            URL = "https://demo.vivapayments.com/web/checkout?ref=%s" % orderCode
            print(URL)
            URL = "https://demo.vivapayments.com/web/checkout?ref=%s" % (self.acquirer_reference)
            if self.acquirer_reference:
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': URL,
                }


    def _send_payment_request(self):
        """ Override of payment to send a payment request to Stripe with a confirmed PaymentIntent.

        Note: self.ensure_one()

        :return: None
        :raise: UserError if the transaction is not linked to a token
        """
        super()._send_payment_request()
        if self.provider != 'vivawallet':
            return

        # Make the payment request to Stripe
        if not self.payment_acquirer_id or not self.payment_acquirer_id.vivawallet_client_id  or not self.vivawallet_client_secret or not self.payment_acquirer_id.vivawallet_source_code:
            raise UserError("Vivawallet: " + _("Please configure Vivawallet Client ID, Secret and Source Code"))
        print ("Calle.................")
        payment_intent = self._stripe_create_payment_intent()
        feedback_data = {'reference': self.reference}
        StripeController._include_payment_intent_in_feedback_data(payment_intent, feedback_data)
        _logger.info("entering _handle_feedback_data with data:\n%s", pprint.pformat(feedback_data))
        self._handle_feedback_data('stripe', feedback_data)

    # def _get_specific_rendering_values(self, processing_values):
    #     """ Override of payment to return Payumoney-specific rendering values.
    #
    #     Note: self.ensure_one() from `_get_processing_values`
    #
    #     :param dict processing_values: The generic and specific processing values of the transaction
    #     :return: The dict of acquirer-specific processing values
    #     :rtype: dict
    #     """
    #     res = super()._get_specific_rendering_values(processing_values)
    #     if self.provider != 'vivawallet':
    #         return res
    #
    #     first_name, last_name = payment_utils.split_partner_name(self.partner_id.name)
    #     api_url = 'https://secure.payu.in/_payment' if self.acquirer_id.state == 'enabled' \
    #         else 'https://sandboxsecure.payu.in/_payment'
    #     vivawallet_values = {
    #         'key': self.acquirer_id.vivawallet_client_id,
    #         'txnid': self.reference,
    #         'amount': self.amount,
    #         'productinfo': self.reference,
    #         'firstname': first_name,
    #         'lastname': last_name,
    #         'email': self.partner_email,
    #         'phone': self.partner_phone,
    #         'return_url': urls.url_join(self.get_base_url(), PayUMoneyController._return_url),
    #         'api_url': api_url,
    #     }
    #     vivawallet_values['hash'] = self.acquirer_id._vivawallet_generate_sign(
    #         vivawallet_values, incoming=False,
    #     )
    #     return vivawallet_values
    #
    # @api.model
    # def _get_tx_from_feedback_data(self, provider, data):
    #     """ Override of payment to find the transaction based on Payumoney data.
    #
    #     :param str provider: The provider of the acquirer that handled the transaction
    #     :param dict data: The feedback data sent by the provider
    #     :return: The transaction if found
    #     :rtype: recordset of `payment.transaction`
    #     :raise: ValidationError if inconsistent data were received
    #     :raise: ValidationError if the data match no transaction
    #     :raise: ValidationError if the signature can not be verified
    #     """
    #     tx = super()._get_tx_from_feedback_data(provider, data)
    #     if provider != 'vivawallet':
    #         return tx
    #
    #     reference = data.get('txnid')
    #     shasign = data.get('hash')
    #     if not reference or not shasign:
    #         raise ValidationError(
    #             "PayUmoney: " + _(
    #                 "Received data with missing reference (%(ref)s) or shasign (%(sign)s)",
    #                 ref=reference, sign=shasign,
    #             )
    #         )
    #
    #     tx = self.search([('reference', '=', reference), ('provider', '=', 'vivawallet')])
    #     if not tx:
    #         raise ValidationError(
    #             "PayUmoney: " + _("No transaction found matching reference %s.", reference)
    #         )
    #
    #     # Verify shasign
    #     shasign_check = tx.acquirer_id._vivawallet_generate_sign(data, incoming=True)
    #     if shasign_check != shasign:
    #         raise ValidationError(
    #             "PayUmoney: " + _(
    #                 "Invalid shasign: received %(sign)s, computed %(computed)s.",
    #                 sign=shasign, computed=shasign_check
    #             )
    #         )
    #
    #     return tx
    #
    # def _process_feedback_data(self, data):
    #     """ Override of payment to process the transaction based on Payumoney data.
    #
    #     Note: self.ensure_one()
    #
    #     :param dict data: The feedback data sent by the provider
    #     :return: None
    #     """
    #     super()._process_feedback_data(data)
    #     if self.provider != 'vivawallet':
    #         return
    #
    #     status = data.get('status')
    #     self.acquirer_reference = data.get('payuMoneyId')
    #
    #     if status == 'success':
    #         self._set_done()
    #     else:  # 'failure'
    #         # See https://www.vivawallet.com/pdf/PayUMoney-Technical-Integration-Document.pdf
    #         error_code = data.get('Error')
    #         self._set_error(
    #             "PayUmoney: " + _("The payment encountered an error with code %s", error_code)
    #         )
