from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    ni_product_description = fields.Char(string="Description")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        res = super(ProductTemplate,self)._get_combination_info(combination,product_id,add_qty,pricelist,parent_combination,only_template)
        product = self.env['product.product'].search([('id','=',res.get('product_id'))],limit=1)
        if product.default_code:
            res.update(
                ni_default_code=product.default_code,
            )
        else:
            res.update(
                ni_default_code='',
            )
        if only_template == False:
            res.update(
                ni_product_description=product.ni_product_description,
            )
        return res
