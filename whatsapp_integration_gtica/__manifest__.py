
# -*- coding: utf-8 -*-
# Copyright 2020 GTICA.C.A. - Ing Henry Vivas
{
    'name': 'Whatsapp Integration All in One',
    'summary': 'Integration Whatsapp for Sale, CRM, Invoice, Delivery and more',
    'version': '13.0.1.0.0',
    'category': 'Administration',
    'author': 'GTICA.C.A',
    'support': 'controlmanager@gtica.online',
    'license': 'OPL-1',
    'website': 'https://gtica.online/',
    'live_test_url': 'http://demo.gtica.online/',
    'price': 41.99,
    'currency': 'EUR',
    'depends': [
        'base',
        'crm',
        'sale_management',
        'sales_team',
        'purchase',
        'account',
        'stock',
    ],
    'data': [
        'data/data_whatsapp_default.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/view_whatsapp_integration_template.xml',
        'views/view_integration_crm.xml',
        'views/view_integration_sale.xml',
        'views/view_integration_purchase.xml',
        'views/view_integration_invoice.xml',
        'views/view_integration_payment.xml',
        'views/view_integration_partner.xml',
        'views/view_integration_stock_picking.xml',
        'wizard/wizard_whatsapp_integration_crm.xml',
        'wizard/wizard_whatsapp_integration_sale.xml',
        'wizard/wizard_whatsapp_integration_purchase.xml',
        'wizard/wizard_whatsapp_integration_invoice.xml',
        'wizard/wizard_whatsapp_integration_payment.xml',
        'wizard/wizard_whatsapp_integration_partner.xml',
        'wizard/wizard_whatsapp_integration_delivery.xml',
        'templates/templates.xml'
    ],
    'qweb': [
        'static/src/xml/website_facebook_chat_live.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'application': True,
    'installable': True,
}
