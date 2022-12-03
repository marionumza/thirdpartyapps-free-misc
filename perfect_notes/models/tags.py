from odoo import models, fields, api
from random import randint


class PerfectTags(models.Model):
    _name = 'perfect.tags'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char()
    perfect_id = fields.Many2one("perfect.notes")
    color = fields.Integer(string='Color', default=_get_default_color)
