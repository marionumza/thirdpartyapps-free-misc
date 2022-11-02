# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License AGPL-3.0 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    "name": "Odoo Show Records",
    "version": "15.0.0.1",
    "summary": "Odoo Show Records from Model View",
    "author": "Atingo - Tadeusz Karpiński",
    "description": """
    """,
    "category": "Extra Tools",
    "website": "https://www.atingo.pl",
    "depends": [
        "base",
    ],
    "data": [
        "views/ir_model_view.xml",
    ],
    "images": [
        "static/description/images/banner.png",
    ],
    "auto_install": True,
    "installable": True,
    "application": False,
    "external_dependencies": {
        "python": [],
    },
    "license": "LGPL-3",
}
