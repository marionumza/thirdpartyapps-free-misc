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
{
    'name': "Lab Test Management",
    'summary': """
     Lab Test and Management for Hospital
        """,
    'description': """
            Lab Test and Management for Hospital""",
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    "license": "AGPL-3",
    'category': 'Hospital',
    'version': '15.0.1.0.0',
    'depends': ['base_hospital_management', 'hr_contract',
                'hr_holidays', 'web_domain_field'
                ],
    'data': [
        'security/ir.model.access.csv',
        'reports/test_report.xml',
        'reports/result.xml',
        'data/lab_sequence.xml',
        'data/test_sequence.xml',
        'data/test_appoin_sequence.xml',
        'data/result_sequence.xml',
        'data/lab_sequence.xml',
        'views/labs.xml',
        'views/lab_test.xml',
        'views/appointment.xml',
        'views/result.xml',
        'views/lab_technician.xml',
        'views/test_type.xml',

    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
