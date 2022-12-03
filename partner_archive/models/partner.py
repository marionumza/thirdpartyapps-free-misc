# Copyright 2018-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        if 'active' in vals and 'skip_active_pop' not in self._context:
            archive = vals.pop('active')
            super(Partner, self).write(vals=vals)
            partners = self.env['res.partner']
            for partner in self:
                partners |= partner.with_context(active_test=False).search([('id','child_of',partner.id)])
            partners.with_context(skip_active_pop=True).write({'active':archive})
        return super(Partner, self).write(vals=vals)
