# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Facebook Product Category',
    'version': '15.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'LGPL-3',
    'summary': 'Assigning Facebook product categories to your Odoo products',
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://apps.garazd.biz/r/55S',
    'depends': [
        'website_sale',
        'base_import_helper',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_facebook_category_views.xml',
        'wizard/base_import_helper_views.xml',
        'data/ir_action_todo_data.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
