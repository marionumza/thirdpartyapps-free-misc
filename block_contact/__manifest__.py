{
    "name": "Block Contact",
    "version": "15.0.2.2",
    "author": "IPGrup",
    "website": "ipgrup.com",
    "category": "Services",
    "depends": ["base", "account", "sale", "stock", "sale_management", "sale_stock"],
    "summary": "Module to block a contact and prevent users from creating quotations, sales or invoices to the blocked contact.",
    "description": "Module to block a contact and prevent users from creating quotations, sales or invoices to the blocked contact. Ideal for business administrators with lots of users or employees.",
    "data": [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/sale_invoice.xml',
        'views/sale_delivery.xml',
        'views/stock_picking_view.xml',
    ],
    "license": "LGPL-3",
    "images": ["static/description/block_contact_banner.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
    'maintainer': """
    IPGrup
    Dídac Alsina - dalsina@ipgrup.cat
    Sergio Peralta - speralta@ipgrup.cat
    """
}