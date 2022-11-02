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
    'name': "Hospital Management",
    'description': """
        Hospital management module which is used to mange the hospital functionalities prescription,patient,doctor diagnosis etc
    """,
    'summary': """
    Hospital management module which is used to mange the hospital functionalities prescription,patient,doctor diagnosis etc
""",
    'author': "Cybrosys Techno Solutions",
    'company': "Cybrosys Techno Solutions",
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    "license": "AGPL-3",
    'category': 'Hospital',
    'version': '15.0.1.0.0',
    'depends': ['base', 'hr', 'account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_prescription_sequence.xml',
        'data/patient_seq.xml',
        'data/diagnosis_seq.xml',
        'data/building_seq.xml',
        'data/test_seq.xml',
        'data/lab_sequence.xml',
        'views/bed.xml',
        'views/wards.xml',
        'views/staff.xml',
        'views/room.xml',
        'views/payment.xml',
        'views/patient_view.xml',
        'views/prescription.xml',
        'views/blood.xml',
        'views/doctor.xml',
        'views/facilities.xml',
        'views/building.xml',
        'views/degree.xml',
        'views/hospital.xml',
        'views/lab.xml',
        'views/vaccine.xml',
        'views/pharmacy.xml',
        'views/vaccination.xml',
        'views/inpatient.xml',
        'views/diagnosis.xml',
        'views/medicine.xml',
        'views/lab_test.xml',
        'views/lab_test_type.xml',
        'views/hospital_labs.xml',
        'wizard/room_assign.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
