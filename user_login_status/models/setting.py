from odoo import models, fields, api


class Setting(models.TransientModel):
    _inherit = 'res.config.settings'

    store_user_time = fields.Boolean(string="Store User Login/Logout Time", default=True)

    def set_values(self):
        res = super(Setting, self).set_values()
        self.env['ir.config_parameter'].set_param('user_login_status.store_user_time',
                                                  self.store_user_time)
        return res

    @api.model
    def get_values(self):
        res = super(Setting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        store_user_time = ICPSudo.get_param('user_login_status.store_user_time')
        res.update(
            store_user_time=store_user_time
        )
        return res
