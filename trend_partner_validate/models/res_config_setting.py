# -*-	coding:	utf-8	-*-
from odoo import models, fields, api


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    apply_mobile_validation = fields.Boolean(string='Apply Mobile & Phone Validation',
                                             help='If Checked Mobile and Phone must be unique per Partner')
    apply_email_validation = fields.Boolean(string='Apply Email Validation',
                                            help='If Checked Email must be unique per Partner')
    apply_tax_validation = fields.Boolean(string='Apply Tax & Company Register Validation',
                                          help='If Checked Tax and Company Register must be unique per Partner')

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('apply_mobile_validation', (self.apply_mobile_validation))
        set_param('apply_email_validation', (self.apply_email_validation))
        set_param('apply_tax_validation', (self.apply_tax_validation))
        super(ConfigSettings, self).set_values()

    def get_values(self):
        res = super(ConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            apply_mobile_validation=bool(get_param('apply_mobile_validation')),
            apply_email_validation=bool(get_param('apply_email_validation')),
            apply_tax_validation=bool(get_param('apply_tax_validation')),
        )
        return res
