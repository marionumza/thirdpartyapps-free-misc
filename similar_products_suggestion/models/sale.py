# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_round
from odoo import SUPERUSER_ID
import datetime as dt
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import http


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self,vals):
        new_id = super(sale_order, self).create(vals)
        line_brw_id = []
        available_products = 0
        suggested_products = False
        if new_id.order_line:
            for line_brw in new_id.order_line:
                if line_brw.product_id.virtual_available > line_brw.product_uom_qty:
                    available_products = available_products + 1
                else:
                    suggested_products = True
                    line_brw_id.append(line_brw)

            if suggested_products:
                customer_template = self.env.ref('similar_products_suggestion.email_template_edi_suggested_product_customer')
                partner_template = self.env.ref('similar_products_suggestion.email_template_edi_suggested_product_user')
                for product in new_id.order_line :
                    if product.product_id.qty_available <= 0:
                        send_customer = customer_template.send_mail(product.id, force_send=True)
                        send_user = partner_template.send_mail(product.id, force_send=True)
        return new_id


class sale_order_line(models.Model):
    _inherit = "sale.order.line"


    def _suggested_product_text(self):
        res={}
        names=""
        for line in self:
            names = [x.name for x in line.product_id.suggested_product_id]
            names = ',\n'.join(names)     
            res[line.id] = names
            line.suggested_product_text = res[line.id]

    suggested_product_text = fields.Char(compute="_suggested_product_text",string="Suggested Product Text")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: