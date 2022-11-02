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
from odoo import api, http
from odoo.http import request


class Employee(http.Controlleron):
    @http.route(['/dashboard'], type='http', auth="public")
    @api.model
    def get_employee_shift(self):
        """Taking employee shifts from the shift modulr"""

        query = """SELECT Count(a.employee_shift_id),a.hr_employee_id,b.name FROM employee_shift_hr_employee_rel as a INNER JOIN hr_employee as b ON 
                a.hr_employee_id=b.id GROUP BY a.hr_employee_id,b.name """

        self._cr.execute(query)
        data = self._cr.dictfetchall()

        name = []
        for record in data:
            name.append(record.get('name'))

        count = []
        for record in data:
            count.append(record.get('count'))

        final = [count, name]
        return request.render("hospital_appointments.appointment_form", final)


