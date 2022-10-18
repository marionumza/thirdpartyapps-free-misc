from odoo import http
from odoo.http import request


class PosProductCreation(http.Controller):

    @http.route('/Add_Product', type="json", auth="none")
    def Add_product(self, category, name, price, uom, type, barcode, **kwargs):
        if type == 'service':
            type = 'service'
        elif type == 'consumable':
            type = 'consu'
        else:
            type = 'product'

        request.env['product.template'].sudo().create({
            'name': name,
            'detailed_type': type,
            'list_price': float(price),
            'categ_id': int(category),
            'uom_id': int(uom),
            'uom_po_id': int(uom),
            'barcode': barcode,
            'available_in_pos': True,
        })
