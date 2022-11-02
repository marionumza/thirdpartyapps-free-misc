# -*- coding: utf-8 -*-
# Copyright 2021 Gusti Tammam
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
# noinspection PyUnresolvedReferences,SpellCheckingInspection
{
    "name": """Asset Sequence Number""",
    "summary": """Provide sequence number support for Odoo Enterprise asset module.""",
    "category": "Accounting",
    "version": "15.0.1.0.0",
    "development_status": "Alpha",  # Options: Alpha|Beta|Production/Stable|Mature
    "auto_install": False,
    "installable": True,
    "application": False,
    "author": "Gusti Tammam",
    "support": "dev@tammam.id",
    # "website": "https://hire.tammam.id",
    "license": "OPL-1",
    "images": [
        'images/main_screenshot.png'
    ],

    # "price": 10.00,
    # "currency": "USD",

    "depends": [
        # odoo addons
        'base',
        'account_asset',
        # third party addons

        # developed addons
    ],
    "data": [
        # group
        # 'security/res_groups.xml',

        # data
        'data/ir_sequence.xml',

        # global action
        # 'views/action/action.xml',

        # view
        'views/common/account_asset.xml',

        # wizard

        # report paperformat
        # 'data/report_paperformat.xml',

        # report template
        # 'views/report/report_template_model_name.xml',

        # report action
        # 'views/action/action_report.xml',

        # assets
        # 'views/assets.xml',

        # onboarding action
        # 'views/action/action_onboarding.xml',

        # action menu
        # 'views/action/action_menu.xml',

        # action onboarding
        # 'views/action/action_onboarding.xml',

        # menu
        # 'views/menu.xml',

        # security
        # 'security/ir.model.access.csv',
        # 'security/ir.rule.csv',

        # data
    ],
    "demo": [
        # 'demo/demo.xml',
    ],
    "qweb": [
        # "static/src/xml/{QWEBFILE1}.xml",
    ],

    "post_load": None,
    # "pre_init_hook": "pre_init_hook",
    # "post_init_hook": "post_init_hook",
    "uninstall_hook": None,

    "external_dependencies": {"python": [], "bin": []},
    # "live_test_url": "",
    # "demo_title": "{MODULE_NAME}",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "{SHORT_DESCRIPTION_OF_THE_MODULE}",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
