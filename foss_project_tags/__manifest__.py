# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Project Tags',
    'version': '15.0.0.0.0',
    'website': 'http://www.fossinfotech.com',
    'category': 'Projects & Tasks',
    'sequence': 14,
    'summary': 'Status Indicators',
    'description': """
        Project Tags
        ==================
        This module adds Projected end dates and Health Indicators to Tasks/Projects.
    """,
    'author':  'FOSS INFOTECH PVT LTD',
    'website': 'www.fossinfotech.com',
    'license': 'Other proprietary',
    'depends': [
        'project','hr_timesheet','web'
    ],
    'data': [
        'views/project_views.xml',
        # 'views/project_status.xml',
            ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            ("foss_project_tags/static/description/css/project_task_state.css")
            
        ]
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/index.html',
    ],
    
    'installable': True,
    'auto_install': False,
    'application': True,
}