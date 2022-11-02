# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017-TODAY Aurium Technologies(<http://www.auriumtechnologies.com>).
#    Author: Jalal ZAHID, Aurium Technologies (<http://www.auriumtechnologies.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, models, fields 

class AccountMove(models.Model):

    _inherit = 'account.move'

    def action_post(self):
        product_obj = self.env['product.product']
        move = super(AccountMove, self).action_post()
        for invoice in self:
            if invoice.move_type in ('in_invoice', 'in_refund'):
                for line in invoice.invoice_line_ids:
                    if line.product_id and line.price_unit:
                        pr_id = product_obj.browse(line.product_id.id)
                        pr_id.write({'standard_price': line.price_unit})
        return move