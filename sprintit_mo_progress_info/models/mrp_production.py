# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2021 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

import logging
logger = logging.getLogger(__name__)

from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    done_workorders_txt = fields.Char('Progress', compute= '_compute_status_mo', help= 'Display from how many work order how much are done till now.')
    
    def _compute_status_mo(self):
        for mo in self:
            done_work_orders = 0
            data = self.env['mrp.workorder'].read_group([
                ('production_id', 'in', self.ids),
                ('state', '=', 'done')], ['production_id'], ['production_id'])
            count_data = dict((item['production_id'][0], item['production_id_count']) for item in data)
            done_work_orders = count_data.get(mo.id, 0)
            mo.done_workorders_txt = str(done_work_orders) + ' / ' + str(len(mo.workorder_ids))