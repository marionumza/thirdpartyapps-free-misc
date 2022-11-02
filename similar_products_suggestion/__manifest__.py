# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name' : "Similar Products Suggestion",
    'version' : "15.0.0.1",
    'category' : "Website",
    'license':'OPL-1',
    'summary': 'Similar Products Suggestion to the customer by email.',
    'description' : '''
            This module adds a feature in product to have suggested products.
			send suggested product by email to customer, product suggestion, item suggestion, website product suggestion, email suggested item. Product send by email. Suggested product send by email, suggested product for customer, Similiar product suggestion for customer, Similiar product suggestion for partner.
    ''',
    'author' : "BrowseInfo",
    'website': 'https://www.browseinfo.in',
    'data': [
             'edi/mail_template_data.xml',
             'views/product_view.xml',
             ],
    'depends' : ['sale_management','stock'],
    'installable': True,
    'auto_install': False,
    "live_test_url":'https://youtu.be/nvsktE5s0Ww',
	"images":['static/description/Banner.png'],

}
