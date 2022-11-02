# -*- coding: utf-8 -*-
# Copyright 2021 Osis.

from odoo.fields import first
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    returned_ids = fields.Many2many(
        "stock.picking",
        compute="_compute_returned_ids",
        string="Returned pickings",
    )
    origin_picking_id = fields.Many2one(
        "stock.picking",
        compute="_compute_picking_id",
        string="Origin",
        store=True
    )

    def _compute_returned_ids(self):
        for picking in self:
            picking.returned_ids = picking.mapped(
                "move_lines.returned_move_ids.picking_id"
            )

    @api.depends("move_lines.origin_returned_move_id")
    def _compute_picking_id(self):
        for picking in self:
            picking.origin_picking_id = first(
                picking.mapped("move_lines.origin_returned_move_id.picking_id")
            )

    def action_view_origin(self):
        return self.origin_picking_id.get_formview_action()
