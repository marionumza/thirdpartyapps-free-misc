# -*- coding: utf-8 -*-

import csv
import logging
import mimetypes

from odoo import fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ImportHelper(models.TransientModel):
    _inherit = 'base_import.helper'

    url = fields.Char(
        default='https://www.facebook.com/products/categories/en_US.txt',
        help='Specify the URL to download a list of product categories (only Plain text .txt)',
        required=True,
    )
    mode = fields.Selection(
        selection_add=[('fb_categ', 'Facebook category')],
    )

    def action_import(self):
        self.ensure_one()
        if self.mode != 'fb_categ':
            return super(ImportHelper, self).action_import()

        else:
            mimetype, encoding = mimetypes.guess_type(self.url)
            if mimetype != 'text/plain':
                raise UserError(_('Only the Plain text (.txt) format is allowed.'))

            res = self.open_url(self.url)
            if res['error']:
                raise UserError(_('Error opening URL: %s') % res['error'])
            content = res['content']

            reader = csv.reader(content.split('\n')[1:], delimiter=',')
            for row in reader:
                vals = {
                    'code': row[0],
                    'name': row[1],
                }
                facebook_category = self.env['product.facebook.category'].search([
                    ('code', '=', vals['code']),
                ])
                if not facebook_category:
                    facebook_category = self.env['product.facebook.category'].create(vals)

            return {
                'name': _('Facebook Categories'),
                'type': 'ir.actions.act_window',
                'res_model': 'product.facebook.category',
                'view_mode': 'tree,form',
                'target': 'current',
            }
