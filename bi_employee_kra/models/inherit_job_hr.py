# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api,_
from odoo.exceptions import UserError


class HR_Job(models.Model):
    _inherit = 'hr.job'



    kra_id = fields.Many2one('hr.kra',string="KRA")

    
