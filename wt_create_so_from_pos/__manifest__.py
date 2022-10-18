{
    'name': 'Create Sales Order From POS',
    'version': '15.0.0.1',
    'category': 'Sales/Point of Sale',
    'summary': 'Create sale order from pos screen and view the sales order created fom pos',
    'description': '''
    ''',
    'author': 'Warlock Technologies Pvt Ltd.',
    'website': 'http://warlocktechnologies.com',
    'support': 'support@warlocktechnologies.com',
    'depends': ['point_of_sale', 'sale_management'],
    "data": ['views/pos_config.xml'],
    'assets': {
        'point_of_sale.assets': [
            'wt_create_so_from_pos/static/src/js/Screens/ProductScreen/ControlButtons/SaleOrderButton.js',
            'wt_create_so_from_pos/static/src/js/Screens/ProductScreen/ControlButtons/ViewSalesOrderButton.js',
            'wt_create_so_from_pos/static/src/js/Screens/SaleOrderScreen/SaleOrderScreen.js',
            'wt_create_so_from_pos/static/src/js/Screens/SaleOrderScreen/ViewSaleOrderList.js',
            'wt_create_so_from_pos/static/src/js/Screens/SaleOrderScreen/ViewSaleOrderRow.js',
            'wt_create_so_from_pos/static/src/js/Popups/SalesOrderPopup.js',
        ],
        'web.assets_qweb': [
            'wt_create_so_from_pos/static/src/xml/**/*',
        ],
    },
    'images': ['static/images/screen_image.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'external_dependencies': {
    },
}
