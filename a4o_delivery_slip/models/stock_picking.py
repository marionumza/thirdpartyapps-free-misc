# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    slip_id = fields.Many2one(
        'delivery.slip', string='Delivery Slip', readonly=True,
        help="Delivery slip in which is this picking.")

    def get_delivery_slip_from_carrier(self):
        ''' Get the delivery slip for pickings from the service provider
        '''
        if not all([x.state == 'done' for x in self]):
            raise UserError(
                _("Some selected pickings are not done!"))
        if not all([x.delivery_type == 'colissimo' for x in self]):
            raise UserError(
                _("Some selected pickings were not sent with Colissimo!"))

        return self[0].carrier_id.get_delivery_slip(self)
