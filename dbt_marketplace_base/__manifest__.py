{
    'name': 'Dreambits Marketplace Base',
    'version': '15.0.1.0.0',
    'depends': ['sale','delivery','queue_job'],
    'summary': 'Module to have Shipment and Shipment Transporter Models',
    'description': """
        This module includes base for integrating various marketplaces into the
        existing odoo ecosystem of Sales Orders and Shipments.

        This module is a must-dependancy for all MarketPlace Integration Modules
        By IndigoERP.
    """,
    'author': 'IndigoERP, Dreambits Technologies Pvt. Ltd.',
    'category': '',
    'website': 'https://indigo-erp.com',
    'demo': [],
    'data': [
        'views/shipment_view.xml',
        'views/stock_picking_view.xml',
        'views/delivery_carrier.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
}

