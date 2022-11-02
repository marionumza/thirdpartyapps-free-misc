# -*- coding: utf-8 -*-
{
    'name': "Employee Books",
    'summary': """
    Core module for employee enhanced features. 
        """,
    'description': """
        Employee Books app enhances the employee standard features with better conroll and performance management. 
    """,
    'author': "Dynexcel",
    'sequence': 60,
    'website': "https://www.dynexcel.com",
    'category': 'Human Resources/Expenses',
    'version': '15.0.0.3',
    'depends': ['hr','hr_contract'],
    'data': [
        'views/emp_books_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpg'],
}
