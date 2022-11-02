# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrContractType(models.Model):
    _name = 'hr.contract.type'
    _description = 'Employee Contract Types'

    name = fields.Char(string="Contract Type", required=True)
    active = fields.Boolean(default=True)
    term_ids = fields.One2many('hr.contract.type.term', 'contract_type_id')


class HrContractTypeTerm(models.Model):
    _name = 'hr.contract.type.term'
    _description = 'Employee Contract Types Terms'

    contract_type_id = fields.Many2one('hr.contract.type')
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    body = fields.Text(required=True)
