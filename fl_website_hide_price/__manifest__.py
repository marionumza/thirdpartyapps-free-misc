# -*- coding: utf-8 -*-

{
    'name': 'Website Hide Price for Not Logged In User',
    'version': '13.0.2.0.0',
    'category': 'Website',
    'summary': 'Hide Price for Not Logged In User in Website Sale, Hide Price in Shop, Hide Product Price, Hide Price for Public Users, Hide Price, Hide prices for public users',
    'description': """
        This module allow to hide price for not logged in user in website sale, 
        Hide prices for public users,
        Hide product price and add to cart button in shop page and product page.
    """,
    'sequence': 1,
    'author': 'Futurelens',
    'website': 'http://thefuturelens.com',
    'depends': ['website_sale'],
    'data': [
        'views/product_price_template.xml'
    ],
    'images': [
        'static/description/banner_website_hide_price.png',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
    'price': 5,
    'currency': 'EUR',
}
