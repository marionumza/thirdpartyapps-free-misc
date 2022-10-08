# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = "product.template"

    product_multi_alias_ids = fields.One2many('product.multi.alias', 'product_tmpl_id', string='Alias')
    product_multi_alias_join = fields.Char(compute='_compute_product_multi_alias_join', store=True, string='Alias')
    product_multi_usage_ids = fields.Many2many('product.multi.usage','product_usage_rel','product_tmpl_id',
                                               'product_usage_id', string='Usos')

    @api.depends('product_multi_alias_ids.name')
    def _compute_product_multi_alias_join(self):
        for rec in self:
            rec.product_multi_alias_join = '\n'.join([a.name for a in rec.product_multi_alias_ids])


class product_product(models.Model):
    _inherit = "product.product"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        #if self._context.get('search_product_multi_alias'):
        if not args:
            args = []
        for index, arg in enumerate(args):
            if arg[0] == "default_code":
                args.insert(index, ('product_multi_alias_join', arg[1], arg[2]))
                args.insert(index, '|')
                break
        return super(product_product, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)


class product_multi_alias(models.Model):
    _name = "product.multi.alias"
    _description = "Product Multi Alias"
    _order = "product_tmpl_id,sequence,id"

    name = fields.Char('Alias', required=True)
    sequence = fields.Integer('Sequence', default=1)
    product_tmpl_id = fields.Many2one('product.template', 'Product', required=True, ondelete="cascade")
    _sql_constraints = [
        ('unique_alias_id', 'unique(product_tmpl_id,alias_id)', 'Alias del producto debe ser unico'),
    ]

class product_multi_usage(models.Model):
    _name = "product.multi.usage"
    _description = "Product Multi Usage"
    _order = "id"

    name = fields.Char(string='Marca', required=True)
    engine = fields.Char(string='Motor')
    model = fields.Char(string="Modelo")
    from_year = fields.Char(string="Año Desde")
    till_year = fields.Char(string="Año Hasta")
    product_ids = fields.Many2many('product.template','product_usage_rel','product_usage_id','product_tmpl_id',string="Productos Relacionados")




