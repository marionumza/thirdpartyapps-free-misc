# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class ShIrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'Ir attachment'

    expiry_date = fields.Date(required=True, default=lambda self: self._context.get(
        'Expiry Date', fields.Date.context_today(self)))

    datas_pdf = fields.Binary(related='datas', string=" ")
    sh_is_notify = fields.Boolean("Expiry Date Notify ??")
    partner = fields.Many2one("res.partner", "Partner")
    email = fields.Char("Email")
    sh_is_send_mail = fields.Boolean("Is Send Mail")
    sh_tag_ids = fields.Many2many("sh.tags",
                                        string="Tags")
