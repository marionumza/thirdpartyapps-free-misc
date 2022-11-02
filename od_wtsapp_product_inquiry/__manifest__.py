{
    'name': "Website Whatsapp Product Inquiry",
    'version': '15.0.0.1',
    'author': 'Odoo Decoder',
    'summary': "Website Whatsapp Product Inquiry",
    'description': """This module add a whatsapp inquiry button near add to cart buttton in odoo ecommerce website. This will help your customers to direct inquiry of products in less time.""",
    'license': 'LGPL-3',
    'website': 'www.odoo.com',
    'category': 'eCommerce',
    'depends': ['website_sale'],
    'data': [
        'views/res_company.xml',
        'views/template.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
}
