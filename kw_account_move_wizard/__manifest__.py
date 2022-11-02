{
    'name': 'Account Journal Cash Move',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '15.0.0.0.2',

    'depends': [
        'account',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'wizard/wizard_journal_move_journal_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
}
