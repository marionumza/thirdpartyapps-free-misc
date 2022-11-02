# See LICENSE file for full copyright and licensing details.
"""Fleet Tenant, Res Partner Model."""

import re
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Res Partner Model."""

    _inherit = "res.partner"

    # is_driver = fields.Boolean(string="Is Driver")
    is_tenant = fields.Boolean(string="Is Tenant")
    # tenant = fields.Boolean(string="Is Tenant?")
    tenancy_ids = fields.One2many('fleet.rent', 'fleet_tenant_id',
                                  string='Fleet Rental Details',
                                  help='Rental Details')
    maintanance_ids = fields.One2many('maintenance.cost', 'tenant_id',
                                      string='Maintenance Details')
    doc_name = fields.Char(string='Filename')
    id_attachment = fields.Binary(string='Identity Proof')

    @api.constrains('mobile')
    def _check_tenant_mobile(self):
        for tenant in self:
            if tenant.mobile:
                if re.match("^\+|[1-9]{1}[0-9]{3,14}$",
                            tenant.mobile) is None:
                    raise ValidationError(
                        _('Please Enter Valid Mobile Number !!'))

    @api.constrains('email')
    def _check_tenant_email(self):
        expr = "^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[a-zA-Z]{2,4}$"
        for tenant in self:
            if tenant.email:
                if re.match(expr, tenant.email) is None:
                    raise ValidationError(
                        _('Please enter valid email address !!'))


class ResUsers(models.Model):
    """Res Users Model."""

    _inherit = "res.users"

    fleet_rent_ids = fields.One2many('fleet.rent', 'tenant_id',
                                     string='Rental Details',
                                     help='Rental Details')
    maintanance_ids = fields.One2many('maintenance.cost', 'tenant_id',
                                      string='Maintenance Details')
