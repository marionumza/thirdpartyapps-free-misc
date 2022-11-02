# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

# Standard library imports
import logging

# Odoo imports
from odoo import models, fields, api

log = logging.getLogger(__name__)


class CustomerAsset(models.Model):
    _name = 'customer.asset'
    _description = 'Customer Asset'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Customer',
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id")
    fsm_task_ids = fields.One2many('project.task', 'customer_asset_id', string='Tasks', readonly=True)
    fsm_task_count = fields.Integer(string='Tasks', compute='_compute_fsm_task_ids')
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")

    def action_view_fsm_task(self):
        action = self.env.ref('sprintit_customer_asset.project_task_action_asset_fsm').read()[0]

        fsm_task_ids = self.mapped('fsm_task_ids')
        action['domain'] = [('id', 'in', fsm_task_ids.ids)]
        return action

    @api.depends('fsm_task_ids')
    def _compute_fsm_task_ids(self):
        for asset in self:
            asset.fsm_task_count = len(asset.fsm_task_ids)

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for asset in self:
            asset.doc_count = Attachment.search_count([('res_model', '=', 'customer.asset'), ('res_id', '=', asset.id)])

    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([
            ('res_model', '=', 'customer.asset'),
            ('res_id', 'in', self.ids),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action
