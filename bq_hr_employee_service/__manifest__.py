{
    'name': 'HR Employee Service',
    'version': "1.0.0",
    'category': 'Human Resources',
    'website': "http://odoobangladesh.com",
    'author':
        'Odoo Bangladesh, ',
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'summary': 'Employee service information & duration',
    'depends': [
        'hr',
    ],
    'external_dependencies': {
        'python': [
            'dateutil',
        ],
    },
    'data': [
        'views/hr_employee.xml',
    ],
}
