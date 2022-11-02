# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'New-Hire Employee Orientation Process in Odoo',
    'version': '15.0.0.0',
    'category': 'human resources',
    'summary': 'App Employee Orientation Process in Odoo Employee Orientation Process employee welcoming Management human resource Employee On-Boarding process Employee OnBoarding Employee welcoming process first day welcome employee orientation checklist HR checklist',
    'description': """Employee orientation Process app is for new employee coming in organization and by selecting orientation checklist
	Workflow:
HR Officer/Manager create Employee orientation (Orientations/Employee Orientations) for new employee coming in organization and by selecting orientation checklist field on orientation form that time it will fill all orientation checklist lines automatically... Now once HR Officer/Manager confirm Employee orientation that time system will create Checklist requests and allocate jobs to responsible person assosicated with that checklist/task.(Orientations/Orientation Checklists Requests)
Now when responsible person login in system, he/she will find job allocated under Orientations/Orientation Checklists Requests and finish it.
Note that Orientation Checklist Configuration will be configured by department, for example new comer join IT department then he/she has going to process under Orientation Checklist Configuration of IT department...
This module allow you to manage employee orientation process
  * Employee Orientations
  * Orientation Checklists Requests
  * Configurations 
Menus:

Orientations
Orientations/Employee Orientations
Orientations/Orientation Checklists Requests
Orientations/Configurations
Orientations/Configurations/Orientation Checklists
Orientations/Configurations/Orientation Checklists Lines
	
	 """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    "price": 8.00,
    "currency": 'EUR',
    'depends': ['base','hr','mail','portal'],
    'data': ['security/ir.model.access.csv',
            'security/groups.xml',
            'views/employee_orientation_line_views.xml',
            'views/checklist_views.xml',
            'views/checklist_request.xml',
            'views/employee_orientation.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
    "license":'OPL-1',
    'live_test_url':'https://www.youtube.com/watch?v=jaa8jDDWt0U&feature=youtu.be',
    "images":['static/description/banner.png'],
}
