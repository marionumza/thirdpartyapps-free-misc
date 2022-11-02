# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
{
    'name': 'Delivery Slip',
    'version': '15.0.0',
    'author': 'Adiczion SARL',
    'category': 'Adiczion',
    'license': 'AGPL-3',
    'depends': [
        'delivery',
    ],
    'demo': [],
    'website': 'http://adiczion.com',
    'description': """
Module Delivery Slip
====================

Adds the ability to manage carrier shipping slips (initially for getting 
delivery slips from Colissimo)

    """,
    'data': [
        #'security/objects_security.xml',
        'security/ir.model.access.csv',
        #'wizard/your_wizard_name.xml',
        #'data/data_for_your_module.xml',
        'views/delivery_slip_views.xml',
        'views/stock_picking_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
