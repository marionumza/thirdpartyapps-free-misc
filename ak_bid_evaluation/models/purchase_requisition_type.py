# -*- coding: utf-8 -*-

from odoo import models, fields, _

class PurchaseRequisitionType(models.Model):
    _inherit = "purchase.requisition.type"

    enable_evaluation = fields.Boolean('Enable Bid Evaluation', 
        help="If this is checked, you will be able to create evaluation records for quotations as part of a tender of this type.")