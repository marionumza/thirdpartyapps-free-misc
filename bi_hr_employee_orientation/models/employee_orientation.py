# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api,_
from odoo.exceptions import Warning, UserError

class Employee_Orientation(models.Model):
    _name = 'employee.orientation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.onchange('employee_id')
    def onchange_employee(self):
        self.department_id = self.employee_id.department_id.id
        self.job_id = self.employee_id.job_id
        self.department_manager_id = self.employee_id.department_id.manager_id.id

        return

    name = fields.Char('Name',readonly=True)
    employee_id = fields.Many2one('hr.employee',string="Employee" ,required=True)
    department_id = fields.Many2one('hr.department',string="Department")
    job_id = fields.Many2one('hr.job',string="Job Position",required=True)
    department_manager_id = fields.Many2one('hr.employee',string="Manager")
    res_user_id = fields.Many2one('res.users',string="Responsible User")
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('done','Done')],string="State",track_visibility='onchange', track_sequence=3,default="draft")
    company_id = fields.Many2one('res.company',string="Comapny")
    date = fields.Date(string="Date")
    checklists_id = fields.Many2one('orientation.checklists',string="Orientation Checklists")
    checklists_requests_ids = fields.One2many('orientation.checklists.requests','orientation_id',string='Checklists Line',readonly=True)
    notes =fields.Text('Notes')

    def unlink(self):
        for order in self:
            if order.state not in ('draft'):
                raise UserError(_('You can not delete a  confirmed orientation.'))
        return super(Employee_Orientation, self).unlink()

    def confirm_visitor(self):
        val = []
        if self.checklists_id.active :
            for line in self.checklists_id.checklists_line_ids :
                val.append((0,0,{'name':line.name,'orientation_id':self.id,'res_user_id':line.res_user_id.id,
                                    'company_id':self.company_id.id,
                                    'date':self.date,
                                    'state':'new',
                                    'user_id' : self.env.user.id}))

            self.sudo().checklists_requests_ids = val

            for i in self.checklists_requests_ids :
                msg_body = _("Hello: %s <br/> You are requested to prepare below checklist. <br/>  ") % (i.res_user_id.name) 
                msg_body += _("Check line : %s <br/>") % (i.name)
                msg_body += _("Employee :  %s <br/>") % (self.employee_id.name)
                if i.expected_date :
                    msg_body += _(" Expected date :  %s <br/>") % (i.expected_date) 
                msg_body += _(" Responsible user :  %s <br/>") % (i.res_user_id.name) 
                msg_body += _(" Thankyou for chooseing %s <br/><br/>") % (i.company_id.name)
                msg_body += _("<table style='border-collapse: collapse;'><tr> %s </tr>") % (i.company_id.name) 
                msg_body += _("<tr> <td>web : %s </td></tr></table>") % (i.company_id.website)

                keval = i.message_post(body=msg_body,partner_ids=[i.res_user_id.partner_id.id])
            self.write({'state': 'confirm'})
        return

    def action_done(self):
        self.write({'state': 'done'})
        return

    @api.model
    def create(self, vals):

        seq = self.env['ir.sequence'].next_by_code('employee.orientation') or '/'
        vals['name'] = seq
        return super(Employee_Orientation, self).create(vals)

class Orientation_checklists_requests(models.Model):
    _name = 'orientation.checklists.requests'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Name',readonly=True)
    orientation_id = fields.Many2one('employee.orientation',string="Orientation",readonly=True )
    res_user_id = fields.Many2one('res.users',string="Responsible User",readonly=True)
    date = fields.Date(string="Date",readonly=True)
    expected_date = fields.Date(string="Expected Date")
    first_attachment = fields.Binary(string = 'First Attachment')
    second_attachment = fields.Binary(string = 'Second Attachment')
    third_attachment =  fields.Binary(string = 'Third Attachment')
    company_id = fields.Many2one('res.company',string="Comapny",readonly=True)
    user_id = fields.Many2one('res.users')

    notes = fields.Text(string="Notes")
    state = fields.Selection([('new','New'),('done','Done')],string="State",track_visibility='onchange', track_sequence=3,default="new")

    def action_done(self):
        self.write({'state': 'done'})
        return

    def unlink(self):
        for order in self:
            if order.state not in ('new'):
                raise UserError(_('You can not delete a  Done requests.'))
        return super(Orientation_checklists_requests, self).unlink()


class Orientation_checklists(models.Model):
    _name = 'orientation.checklists'


    name = fields.Char('Name',required=True)
    department_id = fields.Many2one('hr.department',string="Department")
    active = fields.Boolean(string="Active")
    checklists_line_ids = fields.Many2many('orientation.checklists.line','rel_checklists_id',string='Checklists Line')


class Orientation_checklists_line(models.Model):
    _name = 'orientation.checklists.line'

    name = fields.Char('Name')
    res_user_id = fields.Many2one('res.users',string="Responsible User" ,required=True)
    checklists_id = fields.Many2one('orientation.checklists')



