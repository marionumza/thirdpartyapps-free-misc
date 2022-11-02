# -*- coding: utf-8 -*-
{
	'name': "Organization Chart Premium",
	'summary': """Employee Hierarchy - Multi Company - Drag and Drop - Search - Add - Edit - Delete - Screenshot - Horizontal - Vertical""",
	'description': """Dynamic Display of your Employee Hierarchy""",
	'author': "SLife Organization, Amichia Fréjus Arnaud AKA",
	"website": "https://slifeorganization.com",
	'category': 'Human Resources',
	'version': '2.1',
	'license': 'OPL-1',
	'depends': ['base', 'hr'],
	'price': 25.00,
	'currency': 'EUR',
	'support': 'frejusarnaud@gmail.com',
	'data': [
		'data/slife_org_chart_data.xml',
		'security/ir.model.access.csv',
		'views/org_chart_views.xml',
	],
	'images': [
		'static/src/img/main_screenshot.png'
	],
	'installable': True,
	'application': True,
	'auto_install': False,
	'assets': {
        'web.assets_backend': [
			'org_chart_premium/static/js/org_chart_employee.js',
			'org_chart_premium/static/js/jquery_orgchart.js',
			'org_chart_premium/static/js/other.js',
			'org_chart_premium/static/js/jspdf_min.js',
			'org_chart_premium/static/js/html2canvas_min.js',
			'org_chart_premium/static/src/css/jquery_orgchart.css',
			'org_chart_premium/static/src/css/style.css',
        ],
        'web.assets_qweb': [
            'org_chart_premium/static/src/xml/org_chart_employee.xml',
        ],
    },
}
