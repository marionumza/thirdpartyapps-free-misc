# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Base Document Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Documents Management Account Document Management Customer Document Management Sales Document Management Purchase Document Management Employee Document Management Contact Document Management Project Document Management Task Document Management Odoo",
    "description": """"Base Document Management" is the base module for the document management modules.""",
    "version": "15.0.1",
    'depends': ['base_setup', 'web'],
    'data': [
            'security/ir.model.access.csv',
            'security/base_document_security.xml',
            'views/sh_ir_attachments_views.xml',
            'views/sh_tags.xml',
            ],
    'images': ['static/description/background.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    }
