from odoo import fields, models, api, _
from odoo.exceptions import UserError

class Product(models.Model):
    _inherit = 'res.company'

    def default_code_number(self):
        if self.country_id.phone_code:
            code = self.country_id.phone_code
            return code

    website_whatsapp_number = fields.Char('Whatsapp Number', help='Website Product Inquiry Number must be valid and without sings. Can use the country phone code without plus sign', default=default_code_number)
    whatsapp_message = fields.Text('Whatsapp Message', default='Hello, I want to order this product.', help='Website Product Inquiry Message')
    whatsapp_button_name = fields.Text('Whatsapp Button Name', default='Inquiry', required=True, help='Dynamic Website Product Inquiry Button')

    @api.constrains('website_whatsapp_number')
    def check_website_whatsapp_number(self):
        for rec in self:
            if rec.website_whatsapp_number:
                if ' ' in rec.website_whatsapp_number or '+' in rec.website_whatsapp_number or not rec.website_whatsapp_number.isnumeric() or not len(rec.website_whatsapp_number) > 8:
                    raise UserError(_('Whatsapp Number should be valid number without any space or signs'))
