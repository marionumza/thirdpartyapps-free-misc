# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class POSSessionInherit(models.Model):
    _inherit = 'pos.session'
    _description = 'Backend POS Session'

    def backend_create_order(self):
        # self.env['pos.order'].create({
        #     'session_id': self.id,
        #     'company_id': self.env.company.id,
        #     'state': 'draft',
        # })
        # order_id = self.env['pos.order'].search([('session_id', '=', self.id), ('state', '=', 'draft')]).id
        return {
            'name': _('Create New Order'),
            'res_model': 'pos.order',
            'view_mode': 'form',
            'views': [
                (self.env.ref('backend_pos_by_fas.view_pos_pos_form_backend').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'target': 'new',
            # 'res_id': order_id,
            'domain': [],
            'context': {
                'edit': True,
                'default_company_id': self.env.company.id,
                'default_session_id': self.id,
                'default_pricelist_id': self.config_id.pricelist_id.id,
            },
        }

    def action_view_order_backend(self):
        return {
            'name': _('Orders'),
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
                (self.env.ref('backend_pos_by_fas.view_pos_pos_form_backend').id, 'form'),
                ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
