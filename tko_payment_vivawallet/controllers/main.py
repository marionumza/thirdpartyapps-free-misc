# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class VivaWalletController(http.Controller):
    _success_url = '/payment/vivawallet/success'
    _failure_url = '/payment/vivawallet/unauthorized'

    @http.route(
        _success_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def vivawallet_transaction_successful(self, **data):
        print ("..........data",data)
        # {'t': '5ca8b202-4472-496b-a13f-0b21f8d9f43c', 's': '4300670222143211', 'lang': 'en-GB', 'eventId': '0',
        #  'eci': '2'}

        ## Search transaction:
        acquirer_reference = data.get('s',None)
        if acquirer_reference:
            transaction = request.env['payment.transaction'].sudo().search([('acquirer_reference','=',acquirer_reference)])
            if transaction:
                transaction.write({'state':'done'})
                transaction._cron_finalize_post_processing()
        return request.render("tko_payment_vivawallet.vivawallet_payment_success",{})


    @http.route(
        _failure_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def vivawallet_transaction_unauthorized(self, **data):
        print("fail...........data", data)
        return request.render("tko_payment_vivawallet.vivawallet_payment_unauthorized",{})

