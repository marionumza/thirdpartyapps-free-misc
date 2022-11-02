###################################################################################
# 
#    Copyright (C) Cetmix OÜ
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import _, api, fields, models


class PartnerCategory(models.Model):
    _inherit = "res.partner.category"

    partner_count = fields.Integer(
        string="Partners", compute="_compute_partner_count", store=False
    )
    auto_subscribe = fields.Boolean(
        string="Auto Subscribe",
        help="Auto subscribe newly added partners"
        " to all group records when added to group",
    )
    auto_unsubscribe = fields.Boolean(
        string="Auto Unsubscribe",
        help="Auto unsubscribe partner from all group records if removed from group",
    )

    @api.onchange("auto_subscribe", "auto_unsubscribe")
    def onchange_auto_subscribe(self):
        # -- Ask to purchase Pro version
        if self.auto_subscribe or self.auto_unsubscribe:
            raise models.UserError(_("Please purchase Pro Version to use this feature"))

    @api.depends("partner_ids", "partner_ids.category_id")
    def _compute_partner_count(self):
        """Count Partners in category"""
        for rec in self:
            rec.partner_count = len(rec.partner_ids)

    def name_get(self):
        """Show Partner Count if required"""
        if not self._context.get("partner_count_display", False):
            return super(PartnerCategory, self).name_get()
        return [
            (category.id, "{} ({})".format(category.name, str(category.partner_count)))
            for category in self
        ]
