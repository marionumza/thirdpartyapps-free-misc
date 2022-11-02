# -*- coding: utf-8 -*-

{
    "name": "Simple Payroll",
    "author": "do_project",
    "version": "15.0.1.0.0",
    "category": "Human Resources",
    "depends": [
        "base",
        "hr",
        "hr_attendance",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "view/payslip.xml",
        "view/component.xml",
        "view/attendance.xml",
        "wizard/view_wizard_do_department.xml",
    ],
    "qweb": [
    ],
    "images": ["static/description/icon.jpg","static/description/icon.jpg"],
    "currency": 'EUR',
    "license": 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 150,
}
