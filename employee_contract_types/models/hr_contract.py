# -*- coding: utf-8 -*-
from odoo import models, fields


class HrContract(models.Model):
    _inherit = "hr.contract"

    contract_type_id = fields.Many2one("hr.contract.type", string="Contract Type", ondelete='restrict')

