# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Install Pyscript in Odoo Frontend
#
###################################################################################

{
    "name": "Pyscript",
    "version": "15.0.0.0.1",
    "summary": """ 
            Install Pyscript in Odoo Frontend
            .""",
    "description": """ 
            Install Pyscript in Odoo Frontend
            .""",
    "author": "Cybernetics Plus",
    "website": "https://www.cybernetics.plus",
    "live_test_url": "https://www.cybernetics.plus",
    "images": ["static/description/banner.gif"],
    "category": "Website",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
    "contributors": [
        "Developer <dev@cybernetics.plus>",
    ],
    "depends": [
        "website",
    ],
    "assets": {
        "web.assets_qweb": [
            "https://pyscript.net/latest/pyscript.css",
            "https://pyscript.net/latest/pyscript.js",
        ],
        "web.assets_frontend": [
            "https://pyscript.net/latest/pyscript.css",
            "https://pyscript.net/latest/pyscript.js",
        ],
    },
}
