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
    'name': "Cleaning And Waste Management",
    'summary': """
     Module for Cleaning And Waste Management for a Hospital
        """,
    'description': """
        Module for Cleaning And Waste Management for a hospital""",
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    "license": "AGPL-3",
    'category': 'Hospital',
    'version': '15.0.1.0.0',
    'depends': ['base', 'base_hospital_management', 'hr', 'hospital_cleaning_shifts', 'board',
                ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
        'report/report.xml',
        'report/report_template.xml',
        'views/cleaning_team.xml',
        'views/member_management.xml',
        'views/waste_management.xml',
        # 'views/waste_transfers.xml',
        'views/waste_bin.xml',
        'views/cleaning_inspection.xml',
        'views/waste_request.xml',
        'views/team_members.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hospital_cleaning_waste_management/static/src/css/dashboard.css',
            'hospital_cleaning_waste_management/static/src/css/style.scss',
            'hospital_cleaning_waste_management/static/src/css/material-gauge.css',
            'hospital_cleaning_waste_management/static/src/js/dashboard_view.js',
            'hospital_cleaning_waste_management/static/src/js/lib/Chart.bundle.js',
            'hospital_cleaning_waste_management/static/src/js/lib/highcharts.js',

        ],
        'web.assets_qweb': [
            'hospital_cleaning_waste_management/static/src/xml/dashboard_view.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
