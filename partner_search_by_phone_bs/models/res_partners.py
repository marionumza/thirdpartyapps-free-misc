# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        res = super(ResPartner, self).name_get()
        new_res = []
        for partner in res:
            full_string = partner[1].split("\n")
            partner_phone = self.browse(partner[0]).phone
            partner_mobile = self.browse(partner[0]).mobile
            full_string[0] += " (Ph: " + partner_phone + ")" if partner_phone else ""
            full_string[0] += " (Mb: " + partner_mobile + ")" if partner_mobile else ""
            new_res.append((partner[0], "\n".join(full_string)))
        return new_res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += ['|', '|', ('name', operator, name), ('phone', operator, name), ('mobile', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
