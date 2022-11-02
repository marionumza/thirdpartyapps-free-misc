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
from odoo import fields, models


class InspectionReportWizard(models.TransientModel):
    _name = 'inspection.report.wizard'
    _description = 'inspection_report_wizard'

    inspector = fields.Many2one('res.users')
    cleaning_team = fields.Many2one('cleaning.teams')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def report_action(self):
        domain = []
        inspector = self.inspector
        if inspector:
            domain += [('inspector', '=', inspector.id)]
        date_from = self.date_from
        if date_from:
            domain += [('date', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('date', '<=', date_to)]
        members_id = self.env['cleaning.teams'].search([])
        for rec in members_id.members_ids:
            print(rec.partner_name_id.name)
        cleaning_inspection = self.env['cleaning.inspection'].search_read(domain)
        print(cleaning_inspection,'rrrrrrrrrrrrrrrrrrrr')
        data = {
            'inspector': self.inspector.id,
            'from_date': self.date_from,
            'to_date': self.date_to,
            'cleaning_team':self.cleaning_team.id,
            'cleaning_inspection': cleaning_inspection,
            'form_data': self.read()[0],
        }
        return self.env.ref(
            'hospital_cleaning_waste_management.action_inspection_report').report_action(self,
                                                                        data=data)


class ReportQuery(models.AbstractModel):
    _name = 'report.hospital_cleaning_waste_management.report_inspection'

    def _get_report_values(self, docids, data=None):
        query = '''SELECT a.inspector,a.state,a.date,b.team_name,d.name,f.name as inspector from cleaning_inspection as a INNER JOIN cleaning_teams as b ON a.cleaning_team = b.id
                                INNER JOIN team_category as c ON b.id = c.inverse_id  INNER JOIN hr_employee as d ON c.partner_name_id = d.id
                                INNER JOIN res_users as e ON a.inspector = e.id INNER JOIN res_partner as f ON f.id = e.partner_id '''

        if data['inspector']:
            query = query + """ WHERE a.inspector = '%s'""" % data['inspector']
        if data['from_date']:
            query = query + """ AND a.date >= '%s'""" % data['from_date']
        if data['to_date']:
            query = query + """ AND a.date <= '%s'""" % data['to_date']
        if data['cleaning_team']:
            query = query + """ AND a.cleaning_team = '%s'""" % data['cleaning_team']

        self._cr.execute(query)
        docs = self._cr.dictfetchall()
        return {
            'doc_ids': docids,
            'doc_model': 'cleaning.inspection',
            'cleaning_inspection': docs,
            'data': data,
        }

