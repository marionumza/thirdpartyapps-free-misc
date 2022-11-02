# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class DeliverySlip(models.Model):
    _name = "delivery.slip"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Delivery Slip"

    name = fields.Char(required=True)
    date = fields.Date(string="date of delivery")
    delivery_type = fields.Selection(
        [('none', '')], string='Delivery Type', default='none',
        required=True)
    pickings = fields.One2many(
        'stock.picking', 'slip_id', string='Pickings', readonly=True,
        help="List of pickings in this delivery slip.")
