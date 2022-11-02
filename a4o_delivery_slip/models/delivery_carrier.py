# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def get_delivery_slip(self, pickings):
        ''' Send the package to the service provider

        :param pickings: A recordset of pickings
        :return dict:  containing the information from the slip:
                        {'name': the name of the slip.
                         'date': the date of the slip.
                         'delivery_type': the provider
                         'details': All the details of the slip.
                         'pdf': The slip in pdf format}
        '''
        self.ensure_one()
        if hasattr(self, '%s_get_delivery_slip' % self.delivery_type):
            return getattr(
                self, '%s_get_delivery_slip' % self.delivery_type)(pickings)
        else:
            raise UserError(_("There is not method to get delivery slip for "
                "this service provider: %s !") % self.delivery_type)
