# -*- coding: utf-8 -*-
#@2022 Abdillah Wahab All Right Reserved
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class DoPayslipComponent(models.Model):
    _name = 'do.payslip.component'

    name = fields.Char("Component Name")
    d_category = fields.Selection([('allowance', 'Allowance'), ('deduction', 'Deduction')], 'Category')
    d_component_list = fields.One2many('do.payslip.component.list', 'd_component_id', 'Employees')
    d_type = fields.Selection([('month', 'Monthly'), ('day', 'Daily'), ('onetime', 'One Time')], 'Type')
    d_tax = fields.Boolean('Taxable', default=False)
    d_type_daily = fields.Selection([('none', 'No Check'), ('attendance', 'Check Valid Attendance'), ('fix', 'Fix for a week')], 'Daily Type', default='none')
    d_fix_a_week = fields.Integer('Day / Week')

    def add_all_employee(self, department=None):
        # Do get all Employee and add to Component List
        domain = [('id', 'not in', self.d_component_list.mapped('name').ids)]
        to_write = {}
        if department:
            to_write.update({'name': self.name.split(' [')[0] + " [ " + department.name +' ]'})
            domain.append(('department_id', '=', department.id))
        employee_obj = self.env['hr.employee'].search(domain)
        to_write.update({'d_component_list': self._prepare_list(employee_obj)})
        self.write(to_write)
        return
    
    def _prepare_list(self, employees):
        datas = []
        for emp in employees:
            datas.append((
                0,0, {
                    'name': emp.id,
                    'd_amount': 0,
                }
            ))
        return datas

    def clear_list(self):
        return self.d_component_list.unlink()

    def add_employee_by_department(self):
        # Do department selected and get all employee by this department
        view = self.env.ref('do_simple_payroll.do_view_choose_department_form')
        res = self.env['wizdo.choose.department'].create({'d_component_id': self.id})
        return {
            'name': _("Choose Department"),
            'view_mode': 'form',
            'view_id': view.id,
            'res_id': res.id,
            'view_type': 'form',
            'res_model': 'wizdo.choose.department',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def get_amount_from_contract_salary(self):
        # Loop y employee, and get salary from his/her contract
        for emp_list in self.d_component_list:
            if emp_list.name.contract_id:
                emp_list.d_amount = emp_list.name.contract_id.wage
        return True

    def get_quantity(self, start_date, end_date, employee):
        if self.d_type != "day": return 1
        if self.d_type_daily == 'none':
            return (end_date - start_date).days
        elif self.d_type_daily == 'fix':
            duration = end_date - start_date
            dur = duration.days - (duration.days % 7)
            return (dur / 7) * self.d_fix_a_week
        else:
            attandance = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id), 
                ('check_in', '>=', start_date),
                ('check_in', '<=', end_date),
                ('check_out', '!=', False),
                ('d_validate', '=', 'valid'),
            ])
            return len(attandance)

class DoPayslipComponentList(models.Model):
    _name = 'do.payslip.component.list'

    name = fields.Many2one('hr.employee', 'Employee', required=True)
    d_component_id = fields.Many2one('do.payslip.component', 'Component')
    d_amount = fields.Float('Amount')
