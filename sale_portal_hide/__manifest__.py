# Copyright (C) 2021 TREVI Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Hide Sales Orders and Quotations",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": """TREVI Software,
        Odoo Community Association (OCA)""",
    "summary": """Hide orders &amp; quotations in the customer portal.""",
    "category": "Sales",
    "maintainers": ["TREVI Software"],
    "images": ["static/src/img/main_screenshot.png"],
    "website": "https://github.com/trevi-software/trevi-misc",
    "depends": [
        "portal",
        "sale",
    ],
    "data": [
        "views/sale_portal_templates.xml",
    ],
    "installable": True,
}
