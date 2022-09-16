# -*- coding: utf-8 -*-
{
    'name': 'Minutes Of Meeting',
    'summary': 'Allows you to apply margin percentage globally on the quotation and sales orders.',
    'version': '13.0.1.0.0',
    'category': 'hr',
    'website': 'https://www.abrusnetworks.com',
    'description': """Minutes Of Meeting""",
    'author': 'Abrus Networks',
    'company': 'Abrus Networks',
    'maintainer': 'Abrus Networks',
    'installable': True,
    'depends': [
        'calendar',
        'mail',
        'crm',
    ],
    'demo': [
    ],
    'data': [
        'reports/report.xml',
        'views/minutes_of_meeting.xml',
        'data/mail_template_mom.xml',
        'reports/report_mom.xml',

    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
