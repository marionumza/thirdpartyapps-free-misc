# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)



class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('initial_approve', 'Initial Approve')])


    def button_send_to_approver(self, force=False):
        self.write({'state': 'to approve'})
        return {}

    def button_cancel_request(self):
        self.write({'state': 'cancel'})

    

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'initial_approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True