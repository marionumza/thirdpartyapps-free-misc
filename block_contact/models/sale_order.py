from odoo import api, models, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_block_status = fields.Selection([],readonly = True, store = True, copied = True, related = "partner_id.x_block_user", string = "Blocking Status")

    @api.onchange('partner_id')
    def _onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        partner = self.partner_id

        if partner.x_block_user == 'True':

            for rec in self:
                rec.write({'partner_id': ''})

            return {
                'warning': {
                    'title': _("Blocked contact"),
                    'message': "Cannot create a quotation from a blocked contact.",
                }
            }