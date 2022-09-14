{
    # App information

    'name': "Sale Multiple Products",
    'category': 'Sale',
    'version': '13.0',
    'summary' : 'Save your time by easily manage large Sale Orders through Importing/Mass updating bulk Sales lines in one time',
    'license': 'OPL-1',

    # Author
    'author': 'ShivTech Solutions',
    'website': 'https://www.shivtechsolutions.com',
    'maintainer': 'ShivTech Solutions',

    # Dependencies

    'depends': ['sale'],
    'data': [
        'wizard/select_multi_products.xml',
        'views/sale_order_ext_ept.xml'
    ],

    'images': ['static/description/sale_multi_product_coverpage.jpg'],
    # Technical
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0.00,
    'currency': 'EUR',

}
