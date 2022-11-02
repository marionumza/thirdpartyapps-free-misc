# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
class EmployeeFullName(models.Model):
    _inherit = 'hr.employee'

    emp_fname = fields.Char(string='First Name', copy=True)
    emp_mname = fields.Char(string='Middle Name', copy=True)
    emp_lname = fields.Char(string='Last Name', copy=True)

    @api.onchange('emp_fname','emp_mname','emp_lname')
    def get_employee_name(self):

        for emp_name in self:
            if self.emp_fname:
                fname = self.emp_fname
            else:
                fname = ''
            if self.emp_mname:
                mname = self.emp_mname
            else:
                mname = ''
            if self.emp_lname:
                lname = self.emp_lname
            else:
                lname = ''
            emp_name.name = (str(fname)+' '+str(mname)+' '+str(lname)).title()



class EmployeePublicFullName(models.Model):
    _inherit = 'hr.employee.public'

    emp_fname = fields.Char(readonly=True)
    emp_mname = fields.Char(readonly=True)
    emp_lname = fields.Char(readonly=True)



class PartnerFullName(models.Model):
    _inherit = 'res.partner'

    partner_fname = fields.Char(string='First Name', copy=True)
    partner_mname = fields.Char(string='Middle Name', copy=True)
    partner_lname = fields.Char(string='Last Name', copy=True)

    @api.onchange('partner_fname','partner_mname','partner_lname')
    def get_partner_name(self):

        for p_name in self:
            if self.partner_fname:
                fname = self.partner_fname
            else:
                fname = ''
            if self.partner_mname:
                mname = self.partner_mname
            else:
                mname = ''
            if self.partner_lname:
                lname = self.partner_lname
            else:
                lname = ''
            p_name.name = (str(fname)+' '+str(mname)+' '+str(lname)).title()

class PartnerFullName(models.Model):
    _inherit = 'res.users'

    user_fname = fields.Char(string='First Name', copy=True)
    user_mname = fields.Char(string='Middle Name', copy=True)
    user_lname = fields.Char(string='Last Name', copy=True)

    @api.onchange('user_fname','user_mname','user_lname')
    def get_partner_name(self):

        for u_name in self:
            if self.user_fname:
                fname = self.user_fname
            else:
                fname = ''
            if self.user_mname:
                mname = self.user_mname
            else:
                mname = ''
            if self.user_lname:
                lname = self.user_lname
            else:
                lname = ''
            u_name.name = (str(fname)+' '+str(mname)+' '+str(lname)).title()


