# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductFacebookCategory(models.Model):
    _name = "product.facebook.category"
    _description = 'Facebook Product Category'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
        readonly=True,
    )

    @api.constrains('code')
    def _check_code(self):
        for category in self:
            recs = self.search_count([('code', '=', category.code)])
            if recs > 1:
                raise ValidationError(_('The code of the Facebook category must be unique.'))
