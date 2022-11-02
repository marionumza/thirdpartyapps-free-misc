{
    'name': 'Limit resources creation access',
    'images': [
        'static/description/screenshot1.png',
        'static/description/screenshot2.png',
        'static/description/screenshot3.png',
        'static/description/main_screenshot.png',
    ],
    'version': '13.0.0.1',
    'summary': 'Limit creation access for partners and products to specific users',
    'description': '''
        Limit creation access for partners and products to specific users
    ''',
    'category': 'Resources',
    'author': 'FireBits',
    'license': 'LGPL-3',
    'company': 'FireBits',
    'maintainer': 'FireBits',
    'support': 'support@firebits.net',
    'sequence':-52,
    'website': 'https://firebits.net',
    'live_test_url': 'https://www.youtube.com/firebits',
    'demo': [],
    'depends': [
        'base',
        'product'
    ],
    'data': [
        'security/groups.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}