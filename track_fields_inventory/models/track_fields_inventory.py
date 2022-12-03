from odoo import models, fields
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class TrackFieldsInventory(models.Model):
    _inherit = "product.template"

    name = fields.Char(string='Product Name', track_visibility='always')
    sale_ok = fields.Boolean(string='Can be Sold', track_visibility='always')
    purchase_ok = fields.Boolean(string='Can be Purchased', track_visibility='always')

    # Smart Button
    active = fields.Boolean(string='Active', track_visibility='always')

    # General Information
    type = fields.Selection(string='Product Type', track_visibility='always')
    categ_id = fields.Many2one(string='Product Category', track_visibility='always')
    default_code = fields.Char(string='Internal Reference', track_visibility='always')
    barcode = fields.Char(string='Barcode', track_visibility='always')
    list_price = fields.Float(string='Sales Price', track_visibility='always')
    standard_price = fields.Float(string='Cost', track_visibility='always')
    uom_id = fields.Many2one(string='Unit of Measure', track_visibility='always')
    uom_po_id = fields.Many2one(string='Unit of Measure', track_visibility='always')
    description = fields.Text(string='Description', track_visibility='always')

    # Sales
    description_sale = fields.Text(string='Sale Description', track_visibility='always')
    available_in_pos = fields.Boolean(string='Available in PoS', track_visibility='always')
    to_weight = fields.Boolean(string='To Weigh With Scale', track_visibility='always')
    invoice_policy = fields.Selection([
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')], string='Invoicing Policy',
        help='Ordered Quantity: Invoice quantities ordered by the customer.\n'
             'Delivered Quantity: Invoice quantities delivered to the customer.',
        default='delivery', track_visibility='always')

    # Purchase
    description_purchase = fields.Text(string='Description for Vendors', track_visibility='always')
    purchase_method = fields.Selection([
        ('purchase', 'On ordered quantities'),
        ('receive', 'On received quantities'),
    ], string="Control Policy", default="receive", track_visibility='always')
    service_to_purchase = fields.Boolean("Purchase Automatically", track_visibility='always')
    purchase_line_warn = fields.Selection(WARNING_MESSAGE, 'Purchase Order Line', help=WARNING_HELP, required=True,
                                          default="no-message", track_visibility='always')
    purchase_line_warn_msg = fields.Text('Message for Purchase Order Line', track_visibility='always')

    # Inventory
    sale_delay = fields.Float(string='Customer Lead Time', track_visibility='always')
    weight = fields.Float(string='Weight', track_visibility='always')
    volume = fields.Float(string='Volume', track_visibility='always')
    responsible_id = fields.Many2one(string='Responsible', track_visibility='always')
    property_stock_production = fields.Many2one(string='Production Location', track_visibility='always')
    property_stock_inventory = fields.Many2one(string='Inventory Location', track_visibility='always')
    description_pickingout = fields.Text(string='Description on Delivery Orders', track_visibility='always')
    description_pickingin = fields.Text(string='Description for Receipts', track_visibility='always')
    description_picking = fields.Text(string='Description for Internal Transfers', track_visibility='always')
    tracking = fields.Selection(string='Tracking', track_visibility='always')
    use_time = fields.Integer(string='Product Use Time', track_visibility='always')
    life_time = fields.Integer(string='Product Life Time', track_visibility='always')
    removal_time = fields.Integer(string='Product Removal Time', track_visibility='always')
    alert_time = fields.Integer(string='Product Alert Time', track_visibility='always')
    produce_delay = fields.Float('Manufacturing Lead Time', default=0.0, track_visibility='always')



    # Accounting
    property_account_income_id = fields.Many2one('account.account.template',
                                                 string='Income Account', track_visibility='always')
    property_account_expense_id = fields.Many2one('account.account.template',
                                                  string='Expense Account', track_visibility='always')
    property_account_creditor_price_difference = fields.Many2one(
        'account.account', string="Price Difference Account", track_visibility='always')

