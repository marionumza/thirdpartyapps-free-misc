# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class ShTags(models.Model):
    _name = 'sh.tags'
    _description = 'Sh Tags'
    
    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index', default=1)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    