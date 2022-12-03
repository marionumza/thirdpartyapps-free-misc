# Copyright 2020-2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ilya Ilchenko <https://github.com/mentalko>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Odoo2odoo Integration""",
    "summary": """External Odoo integration powered by Sync Studio""",
    "category": "Extra Tools",
    "images": ["images/sync_odoo2odoo.jpg"],
    "version": "15.0.1.0.0",
    "application": False,
    "author": "IT Projects Labs, Ilya Ilchenko",
    "support": "help@itpp.dev",
    "website": "https://itpp.dev/",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["sync"],
    "external_dependencies": {"bin": []},
    "data": [
        "data/sync_project_data.xml",
    ],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
