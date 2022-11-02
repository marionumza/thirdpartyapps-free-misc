# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Company(models.Model):
    _inherit = 'res.company'

    user_id_selection = fields.Selection([('by_default', 'By Default'),
                                          ('by_day', 'By Day'),
                                          ('by_state', 'By State'),
                                          ('by_website', 'By Website')],
                                         'Select Salesperson')
    default_user_id = fields.Many2one('res.users', "Salesperson")
    day_ids = fields.One2many('days.selection', 'company_id', string="Configure Days")
    line_state_ids = fields.One2many('res.state.selection', 'company_id', string="Configure State")
    website_ids = fields.One2many('website.selection', 'company_id', string="Configure Website")
    existing_order_bool = fields.Boolean("Existing Order's Salesperson",
                                         help="If any new order arrives from your existing customer then it will "
                                              "auto-select the Salesperson from last sale order of same customer.")

    @api.constrains('user_id_selection')
    def _check_parent_id(self):
        if self.user_id_selection == 'by_default' and not self.default_user_id:
            raise UserError(_('Salesperson is required'))
        if self.user_id_selection == 'by_day' and not self.day_ids:
            raise UserError(_('Salesperson is required with Day'))
        if self.user_id_selection == 'by_state' and not self.line_state_ids:
            raise UserError(_('Salesperson is required with State'))
        if self.user_id_selection == 'by_website' and not self.website_ids:
            raise UserError(_('Salesperson is required with Website'))


class DaySelection(models.Model):
    _name = 'days.selection'
    _description = "Days Selection"
    _sql_constraints = [('days_company_uniq', 'unique (day_selection,company_id)', 'Duplicate Days not allowed !'),
                        ('check_day_user', "check(user_id IS NOT NULL AND day_selection IS NOT NULL)",
                         'Days require a Salesperson')]

    day_selection = fields.Selection([('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'),
                                      ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')],
                                      string='Week Day', required=True)
    user_id = fields.Many2one('res.users', "Salesperson", required=True)
    company_id = fields.Many2one('res.company', "Company")


class StateSelection(models.Model):
    _name = 'res.state.selection'
    _description = "State Selection"
    _sql_constraints = [('check_state_user', "check(user_id IS NOT NULL)",
                         'State require a Salesperson')]

    res_state_ids = fields.Many2many('res.country.state', 'state_selection_rel', string="State", required=True)
    user_id = fields.Many2one('res.users', "Salesperson", required=True)
    company_id = fields.Many2one('res.company', "Company")

    def create(self, vals_list):
        company = self.env.company
        existing_state = company.line_state_ids.filtered(lambda l: l.res_state_ids).mapped('res_state_ids')
        res = super(StateSelection, self).create(vals_list)
        for rec in res:
            if rec.res_state_ids:
                for state in rec.res_state_ids:
                    if state.id in existing_state.ids:
                        raise UserError(_("State %s already defined!" % (state.name)))
        return res

    def write(self, vals):
        company = self.env.company
        st_lst = []
        for line in company.line_state_ids:
            if line.res_state_ids:
                st_lst = st_lst + line.res_state_ids.ids
        for rec in self:
            if rec.res_state_ids:
                state = []
                for element in vals.get('res_state_ids')[0][2]:
                    if element not in rec.res_state_ids.ids:
                        state.append(element)
                        if state[0] in st_lst:
                            state_id = self.env['res.country.state'].browse(state[0])
                            raise UserError(_("State %s already defined!" %(state_id.name)))
        return super(StateSelection, self).write(vals)


class WebsiteSelection(models.Model):
    _name = 'website.selection'
    _description = "Website Selection"
    _sql_constraints = [('website_company_uniq', 'unique (website_id,company_id)', 'Duplicate Website not allowed !'),
                        ('check_website_user', "check(user_id IS NOT NULL AND website_id IS NOT NULL)",
                         'Website require a Salesperson')]

    website_id = fields.Many2one('website', "Website", required=True)
    user_id = fields.Many2one('res.users', "Salesperson", required=True)
    company_id = fields.Many2one('res.company', "Company")
