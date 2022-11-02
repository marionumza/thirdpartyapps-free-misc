# -*- coding: utf-8 -*-
from odoo import fields, models


class count_order_move(models.Model):
    _inherit = 'sale.order'

    def _compute_order_move_lines(self):
        self.move_count = self.env['stock.move'].search_count([('origin', '=', self.name)])

    move_count = fields.Integer(
        string='Count Moves', compute='_compute_order_move_lines')

    def action_view_count_stock_moves(self):
        action = self.env.ref('sale_order_stock_moves.stock_move_action').read()[0]
        move = self.env['stock.move'].search([('origin', '=', self.name)])
        if len(move) > 1:
            action['domain'] = [('id', 'in', move.ids)]
        elif move:
            action['views'] = [(self.env.ref('stock.view_move_form').id, 'form')]
            action['res_id'] = move.id
        return action
