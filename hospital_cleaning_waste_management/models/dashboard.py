# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, api


class EmployeeShift(models.Model):
    _inherit = 'employee.shift'

    @api.model
    def get_count_unassigned(self):
        """taking the employee shifts who are cleaning department"""
        count_unassigned = self.env['employee.shift'].search_count(
            [('department_id', '=', 'Cleaning')])

        return {'count_unassigned': count_unassigned}

    @api.model
    def get_employee_shift(self):
        """taking count of employee shifts"""
        query = """SELECT Count(a.employee_shift_id),a.hr_employee_id,b.name,c.name FROM 
        employee_shift_hr_employee_rel as a INNER JOIN hr_employee as b ON a.hr_employee_id=b.id   INNER JOIN 
        employee_shift as c  ON a.employee_shift_id = c.id GROUP BY a.hr_employee_id,b.name,c.name """

        self._cr.execute(query)
        data = self._cr.dictfetchall()

        name = []
        for record in data:
            name.append(record.get('name'))

        count = []
        for record in data:
            count.append(record.get('count'))

        final = [count, name]
        return final

    @api.model
    def get_shift(self):
        """taking the employee shift"""
        self._cr.execute('''SELECT Count(a.employee_shift_id),
        a.hr_employee_id,b.name,c.name FROM employee_shift_hr_employee_rel as 
        a INNER JOIN hr_employee as b ON a.hr_employee_id=b.id   INNER JOIN 
        employee_shift as c  ON a.employee_shift_id = c.id GROUP BY 
        a.hr_employee_id,b.name,c.name''')
        data1 = self._cr.fetchall()

        top_revenue = []
        for rec in data1:
            rec_list = list(rec)
            top_revenue.append(rec_list)

        return {'top_revenue': top_revenue}

    @api.model
    def get_employee_shift_count(self):
        """getting each employee's shift count"""
        query = """SELECT Count(B.employee_shift_id),A.name from 
        employee_shift_hr_employee_rel as B INNER JOIN hr_employee as A ON 
        B.hr_employee_id = A.id group by A.name """

        self._cr.execute(query)
        data = self._cr.dictfetchall()
        name = []
        for record in data:
            name.append(record.get('name'))
            print(record,'record')

        count = []
        for record in data:
            count.append(record.get('count'))
        shift_count = [count, name]
        print(shift_count,'shift_count')
        return shift_count


class EmployeeDepartment(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def get_dept_employee(self):
        """getting employee department"""
        cr = self._cr
        cr.execute("""select department_id, hr_department.name,count(*) from 
        hr_employee join hr_department on 
        hr_department.id=hr_employee.department_id group by 
        hr_employee.department_id,hr_department.name""")
        dat = cr.fetchall()
        data = []
        for i in range(0, len(dat)):
            data.append({'label': dat[i][1], 'value': dat[i][2]})
        return data


