# -*- coding: utf-8 -*-

import base64
import io
import sys

from PIL import Image

from odoo import _, api, exceptions, fields, models
from odoo.tools.mimetypes import guess_mimetype


class AnitaPwaSetting(models.TransientModel):
    """
    """
    _inherit = "res.config.settings"

    enable_pwa = fields.Boolean(string="Enable PWA", default=True)
    pwa_type = fields.Selection(
        selection=[('system', 'System'), ('company', 'company')],
        string='PWA Type', default='system')

    pwa_name = fields.Char(
        string="PWA Name", 
        help="Name of the Progressive Web Application")
        
    pwa_short_name = fields.Char(
        string="PWA Short Name",
        help="Short Name of the Progressive Web Application",)

    pwa_icon_128 = fields.Binary("Icon128", attachment=True)
    pwa_icon_144 = fields.Binary("Icon144", attachment=True)
    pwa_icon_152 = fields.Binary("Icon152", attachment=True)
    pwa_icon_192 = fields.Binary("Icon192", attachment=True)
    pwa_icon_256 = fields.Binary("Icon256", attachment=True)
    pwa_icon_512 = fields.Binary("Icon512", attachment=True)

    pwa_background_color = fields.Char("Background Color")
    pwa_theme_color = fields.Char("Theme Color")

    @api.model
    def get_values(self):
        res = super(AnitaPwaSetting, self).get_values()

        config = self.get_anita_pwa_config_record()
        res["pwa_name"] = config.pwa_name
        res["pwa_short_name"] = config.pwa_short_name
        
        res["pwa_icon_128"] = config.pwa_icon_128
        res["pwa_icon_144"] = config.pwa_icon_144
        res["pwa_icon_152"] = config.pwa_icon_152
        res["pwa_icon_192"] = config.pwa_icon_192
        res["pwa_icon_256"] = config.pwa_icon_256
        res["pwa_icon_512"] = config.pwa_icon_512

        res["pwa_background_color"] = config.pwa_background_color
        res["pwa_theme_color"] = config.pwa_theme_color

        return res

    def _unpack_icon(self, icon):
        """
        unpakc icon
        """
        # Wrap decoded_icon in BytesIO object
        decoded_icon = base64.b64decode(icon)
        icon_bytes = io.BytesIO(decoded_icon)
        return Image.open(icon_bytes)

    def check_image_type(self, icon):
        """
        Check image type
        """
        # Fail if icon provided is larger than 2mb
        if sys.getsizeof(icon) > 2196608:
            raise exceptions.UserError(_("You can't upload a file with more than 2 MB."))

        # Confirm if the pwa_icon binary content is an SVG or PNG
        decoded_pwa_icon = base64.b64decode(icon)
        
        # Full mimetype detection
        pwa_icon_mimetype = guess_mimetype(decoded_pwa_icon)
        if not pwa_icon_mimetype.startswith("image/svg") \
            and not pwa_icon_mimetype.startswith("image/png"):
            raise exceptions.UserError(_("Only Allow SVG Or PNG Files. Found: %s.")
                % pwa_icon_mimetype)

    def get_anita_pwa_config_record(self):
        """
        get config
        """
        # get type form ir.config_parameter
        pwa_type = self.env["ir.config_parameter"].sudo().get_param('anita_pwa.pwa_type', 'system')
        if pwa_type == 'system':
            return self.env["anita_pwa.setting_data"].get_system_config()
        else:
            return self.env["anita_pwa.setting_data"].get_company_config()

    def get_anita_pwa_config(self):
        """
        get antia pwa config
        """
        config = self.get_anita_pwa_config_record()
        values = config.read()[0]
        
        # convert to urls
        if config.pwa_icon_128:
            values["pwa_icon_128"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_128'.format(var_id=config.id)
        else:
            # the static image
            values["pwa_icon_128"] = '/anita_pwa/static/src/img/icon128x128.png'

        if config.pwa_icon_144:
            values["pwa_icon_144"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_144'.format(var_id=config.id)
        else:
            # the static image
            values["pwa_icon_144"] = '/anita_pwa/static/src/img/icon144x144.png'

        if config.pwa_icon_152:
            values["pwa_icon_152"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_152'.format(
                var_id=config.id)
        else:
            # the static image
            values["pwa_icon_152"] = '/anita_pwa/static/src/img/icon152x152.png'

        if config.pwa_icon_192:
            values["pwa_icon_192"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_192'.format(
                var_id=config.id)
        else:
            # the static image
            values["pwa_icon_192"] = '/anita_pwa/static/src/img/icon192x192.png'

        if config.pwa_icon_256:
            values["pwa_icon_256"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_256'.format(
                var_id=config.id)
        else:
            # the static image
            values["pwa_icon_256"] = '/anita_pwa/static/src/img/icon256x256.png'

        if config.pwa_icon_512:
            values["pwa_icon_512"] = '/web/image/anita_pwa.setting_data/{var_id}/pwa_icon_512'.format(
                var_id=config.id)
        else:
            # the static image
            values["pwa_icon_512"] = '/anita_pwa/static/src/img/icon512x512.png'

        return values

    def set_values(self):
        """
        Set values
        """
        res = super(AnitaPwaSetting, self).set_values()
        
        # save enable pwa and pwa type to ir.config_parameter
        self.env["ir.config_parameter"].sudo().set_param('anita_pwa.enable_pwa', self.enable_pwa)
        self.env["ir.config_parameter"].sudo().set_param('anita_pwa.pwa_type', self.pwa_type)

        config = self.get_anita_pwa_config_record()

        config.pwa_name = self.pwa_name
        config.pwa_short_name = self.pwa_short_name
        config.pwa_background_color = self.pwa_background_color
        config.pwa_theme_color = self.pwa_theme_color

        if self.pwa_icon_128:
            self.check_image_type(self.pwa_icon_128)
            config.pwa_icon_128 = self.pwa_icon_128
        
        if self.pwa_icon_144:
            self.check_image_type(self.pwa_icon_144)
            config.pwa_icon_144 = self.pwa_icon_144

        if self.pwa_icon_152:
            self.check_image_type(self.pwa_icon_152)
            config.pwa_icon_152 = self.pwa_icon_152

        if self.pwa_icon_192:
            config.pwa_icon_192 = self.pwa_icon_192

        if self.pwa_icon_256:
            self.check_image_type(self.pwa_icon_256)
            config.pwa_icon_256 = self.pwa_icon_256

        if self.pwa_icon_512:
            self.check_image_type(self.pwa_icon_512)
            config.pwa_icon_512 = self.pwa_icon_512
    
        return res

    def is_pwa_enabled(self):
        """
        Is PWA enabled
        """
        enable_pwa = self.env["ir.config_parameter"].sudo().get_param('anita_pwa.enable_pwa', True)
        return enable_pwa
