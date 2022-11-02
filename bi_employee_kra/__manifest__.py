# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "HR Employee Performance report KRA/KPA in Odoo",
    "version" : "15.0.0.0",
    "category" : "Human Resources",
    'summary': 'Apps for Human Resource productivity report Employee Performance Evaluation by KRA Employee Value Rating  Employee Performance Evaluation by KPA employee KRA report employee efficiency report HR KRA report HR Performance KPA Employee KRA Performance',
    "description": """
    
    Employee Performance Evaluation by KRA/Value Rating
    KRA report 
    kPA
    Value Rating
    Human Resource KRA report
    Human Resource productivity report
    hr employee efficiency report
    employee efficiency report
    Performance Evaluation report
    employee Performance Evaluation report
    hr report employee efficiency report
    hr employee Performance Evaluation report
    hr employee Evaluation report
    employee Evaluation report
    hr KRA report
    kra report 
    employee efficiency report
    staff performance report
    employee productivity report
    hr staff productivity report
    staff efficiency report 
    kra hr report
    employee value rating report
    kra value rating report
    hr kra value rating report


   Description of the module. 

    
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 19,
    "currency": 'EUR',
    "depends" : ['base','hr'],
    "data": [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'wizard/wizard_kra_view.xml',
        'views/kra_views.xml',
        'views/job_inherit_views.xml',
        'views/employee_kra_view.xml',
        'views/value_rating_views.xml',
        'views/report_views.xml',
        'report/kra_report.xml',
        'report/report_views.xml',
        'report/value_report.xml',
    ],
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "license":'OPL-1',
    "live_test_url":'https://youtu.be/GNj-HJhoEkU',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
