# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payroll Sales Commission',
    'version': '15.0',
    'category': 'HR / Payroll',
    'summary': 'Pay your employees commissions with payroll',
    'description': """Pay your employees commissions with payroll""",
    'depends': ['sale_management', 'hr_payroll'],
    'author': 'OdooBot',
    'license': 'OPL-1',
    'website': 'odoobot.8069@gmail.com',
    'price': 0,
	'currency': "EUR",
    'images': [
        'static/src/img/screenshot.png',
    ],
    'data': [
        'views/hr_views.xml',
        'views/sale_views.xml',
    ],
    'application': False,
}
