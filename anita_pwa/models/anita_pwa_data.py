# -*- coding: utf-8 -*-

import base64
from odoo.modules.module import get_resource_path

from odoo import _, api, fields, models


class AnitaPwaSettingData(models.Model):
    """
    """
    _name = "anita_pwa.setting_data"
    _description = "Anita PWA Setting Data"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company", 
        required=False,
        help="If it is not set, it is the system config.")

    pwa_name = fields.Char(
        string="PWA Name", 
        default="Anita PWA",
        help="Name of the Progressive Web Application")

    pwa_short_name = fields.Char(
        string="PWA Short Name",
        default="Anita",
        help="Short Name of the Progressive Web Application",)

    def _get_default_icon(self, size=512):
        """
        Get the default icon
        :param size:
        :return:
        """
        tmp_path = get_resource_path(
            'anita_pwa', 'static', 'icons', 'icon-{size}x{size}.png'.format(size=size))
        return base64.b64encode(open(tmp_path, 'rb') .read())

    pwa_icon_128 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(128),
        attachment=True)
    pwa_icon_144 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(144),
        attachment=True)
    pwa_icon_152 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(152),
        attachment=True)
    pwa_icon_192 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(192),
        attachment=True)
    pwa_icon_256 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(256),
        attachment=True)
    pwa_icon_512 = fields.Binary(
        "Icon", 
        default=lambda self: self._get_default_icon(512),
        attachment=True)

    pwa_background_color = fields.Char(
        string="Background Color", default="#2E69B5")
    pwa_theme_color = fields.Char(
        string="Theme Color", default="#2E69B5")

    @api.model
    def get_company_config(self):
        """
        Get the company config
        :return:
        """
        company_id = self.env.user.company_id.id
        record = self.env["res.config.settings"].search(
            [("company_id", "=", company_id)])
        if not record:
            record = self.env["res.config.settings"].create({
                "company_id": company_id,
            })
        return record

    @api.model
    def get_system_config(self):
        """
        Get the system config
        :return:
        """
        record = self.env["anita_pwa.setting_data"].search(
            [("company_id", "=", False)])
        if not record:
            record = self.sudo().create([{
                "company_id": False,
            }])
        return record
