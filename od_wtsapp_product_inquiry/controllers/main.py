from odoo import http
from odoo.http import request
import werkzeug
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleController(WebsiteSale):

    @http.route(['/whatsapp/redirect/inquiry/<int:product>'], type='http', auth="public", website=True)
    def whatsapp_product_inquiry(self, **kw):
        if kw and kw.get('product'):
            product = request.env['product.product'].sudo().browse(int(kw.get('product')))
            if product and request.env.company:
                website = request.env['website'].get_current_website()
                product_url = website.get_base_url()+product.website_url
                dynamic_message = str('\n*Product Details*\n' +
                '*Name :* %s' %(product.display_name)+
                '\n*Price :* %s' %(product.lst_price)+
                '\n*URL :* %s' %(product_url))
                message = request.env.company.whatsapp_message + dynamic_message
                url = "https://wa.me/%s?text=%s" %(request.env.company.website_whatsapp_number, message)
                return werkzeug.utils.redirect(url)
