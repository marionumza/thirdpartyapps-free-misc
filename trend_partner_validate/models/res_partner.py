# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_register = fields.Char(string="Company Register", required=False, )

    @api.constrains('mobile', 'phone')
    def check_mobile_and_phone_value(self):
        should_verify = self.env['ir.config_parameter'].sudo().get_param('apply_mobile_validation')
        if not should_verify:
            return
        for partner in self:
            numbers = []
            if partner.mobile:
                numbers.append(partner.mobile[-10:])
            if partner.phone:
                numbers.append(partner.phone[-10:])
            numbers = tuple(numbers)
            if not numbers:
                return True
            query = """
            SELECT id FROM  res_partner 
            WHERE id != %s
            AND (RIGHT(mobile, 10) in %s OR RIGHT(phone, 10) in %s) ;
            """
            self._cr.execute(query, (partner.id, numbers, numbers))
            partner_objects = self._cr.fetchall()
            if partner_objects:
                raise ValidationError(_('Mobile and phone must be unique value.'))

    @api.constrains('email')
    def check_email_value(self):
        should_verify = self.env['ir.config_parameter'].sudo().get_param('apply_email_validation')
        if not should_verify:
            return

        for partner in self:
            if not partner.email:
                return True
            partners = self.search_count([('id', '!=', partner.id), ('email', 'ilike', partner.email)])
            if partners:
                raise ValidationError(_('Email is already exists'))

    @api.constrains('vat', 'company_register')
    def check_vat_and_register_value(self):
        should_verify = self.env['ir.config_parameter'].sudo().get_param('apply_tax_validation')
        if not should_verify:
            return

        for partner in self:
            if not partner.vat and not partner.company_register:
                return True

            if partner.vat and self.search_count([('id', '!=', partner.id), ('vat', '=', partner.vat)]):
                raise ValidationError(_('Tax ID must be unique value.'))

            if partner.company_register and self.search_count(
                    [('id', '!=', partner.id), ('company_register', '=', partner.company_register)]):
                raise ValidationError(_('Company Register must be unique value.'))
