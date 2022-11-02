{
    'name': 'Form Disable Quick Edit',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Form Disable Quick Edit',
    'author': 'Lean Easy',
    'website': "https://www.leaneasy.co.uk",
    'depends': ['web'],
    'data': [],
    'images': [
        'static/description/module_banner.png',
        'static/description/icon.png'
    ],
    'assets': {
        'web.assets_backend': [
            'le_form_disable_quick_edit/static/src/js/form_controller.js',
            'le_form_disable_quick_edit/static/src/js/list_renderer.js',
            'le_form_disable_quick_edit/static/src/js/relational_fields.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 0.00,
    'currency': 'EUR',
    'license': 'OPL-1',
}
