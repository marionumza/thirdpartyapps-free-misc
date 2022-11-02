# -*- coding: utf-8 -*-
################################################################################# 
#
#    Author: Abdullah Khalil. Copyrights (C) 2022-TODAY reserved. 
#    Email: abdulah.khaleel@gmail.com
#    You may use this app as per the rules outlined in the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3. 
#    See <http://www.gnu.org/licenses/> for more detials.
#   
#
################################################################################# 

{
    'name': "Bid Evaluation",   
    'summary': "Evaluate and score bids",   
    'description': """
        This app allows you to evaluate individual bids recieved as part of a 
        tender or a purchase agreement. It also provides the ablitity to
        create and use multiple evaluation templates, and setup each template
        with its own set of guidelines, checklists and evaluation/scoring criteria.
    """,   
    'author': "Abdullah Khalil",
    'website': "https://github.com/abdulah-khaleel",
    'category': 'Purchase',
    'version': '15.0.0.0',
     "license": "LGPL-3",
    'depends': ['base','purchase','purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_requisition_type.xml',
        'views/bid_evaluation_template.xml',
        'views/purchase_requisition.xml',
        'views/purchase_order.xml',
        'views/bid_evaluation.xml',
        'views/res_config_settings_views.xml',
        'reports/bid_evaluation_sheet.xml',
        'reports/bids_checklist_summary.xml',
        'reports/bids_evaluation_summary.xml',
        'reports/bids_comparative_report.xml',
    ],
    'images': ["static/description/banner-v15.png"],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
} 
