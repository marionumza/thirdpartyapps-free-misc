from odoo import models, fields, api
import re


class PerfectNotes(models.Model):
    _name = 'perfect.notes'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Perfect Notes"

    name = fields.Char(required=True)
    level_of_difficult = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                          'Level of difficult')
    category_id = fields.Many2one('category.category', 'Category')
    subcategory_id = fields.Many2one('subcategory.subcategory', 'Subcategory')
    tag_ids = fields.Many2many('perfect.tags', 'perfect_id', string='Tags', required=True)
    description = fields.Html("Description")
    summary = fields.Char(compute="compute_summary")
    like_user_ids = fields.Many2many('res.users', string='Liked Users')
    liked_user = fields.Boolean(compute='compute_liked_user')

    @api.depends("summary")
    def compute_summary(self):
        for rec in self:
            rec.summary = None
            result = re.sub("<.*?>", "", rec.description)
            if result and isinstance(result, str):
                if result.__len__() <= 150:
                    rec.summary = result
                else:
                    rec.summary = result[:150] + "..."

    def add_like(self):
        active_user = self.env['res.users'].browse(self._context.get('uid'))
        self.sudo().like_user_ids += active_user

    def delete_like(self):
        active_user = self.env['res.users'].browse(self._context.get('uid'))
        self.sudo().like_user_ids -= active_user

    @api.depends('liked_user')
    def compute_liked_user(self):
        active_user = self.env['res.users'].browse(self._context.get('uid'))
        for rec in self:
            if active_user in rec.like_user_ids:
                rec.liked_user = True
            else:
                rec.liked_user = False
