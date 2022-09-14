# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Product Internal Reference',
    'version': '13.1.0.0',
    'category': 'Website',
    "sequence":  1,
    "author":  "Nevioo Technologies",
    "website":  "www.nevioo.com",
    "license": 'OPL-1',
    "images": ['static/description/Banner.gif'],
    'summary': "Show internal reference/default code and descriptions product variant wise on website.",
    'description': """Show internal reference/default code and descriptions product variant wise on website.""",
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/ni_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
