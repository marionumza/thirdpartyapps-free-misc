from odoo import api, fields, models
from datetime import datetime


class ChangePrize(models.Model):
    _inherit = 'product.template'

    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        track_visibility='always',
        help="Price at which the product is sold to customers.",
    )

    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        track_visibility='always',
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Price', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the next unit that will leave the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
    ], required=True,
        track_visibility='always',
        inverse='_inverse_type',
        help="Select 'Sale' for customer invoices journals.\n" \
             "Select 'Purchase' for vendor bills journals.\n" \
             "Select 'Cash' or 'Bank' for journals that are used in customer or vendor payments.\n" \
             "Select 'General' for miscellaneous operations journals.")

    code = fields.Char(string='Short Code', size=5, required=True, track_visibility='always',
                       help="Shorter name used for display. The journal entries of this journal will also be named using this prefix by default.")

    default_account_id = fields.Many2one(
        comodel_name='account.account', check_company=True, copy=False, ondelete='restrict',
        string='Default Account',
        track_visibility='always',
        domain="[('deprecated', '=', False), ('company_id', '=', company_id),"
               "'|', ('user_type_id', '=', default_account_type), ('user_type_id', 'in', type_control_ids),"
               "('user_type_id.type', 'not in', ('receivable', 'payable'))]")




class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'mail.thread']

    name = fields.Char('Name', index=True, required=True, track_visibility='always', )
    property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], string="Costing Method",
        company_dependent=True, track_visibility='always', copy=True, required=True,
        help="""Standard Price: The products are valued at their standard cost defined on the product.
            Average Cost (AVCO): The products are valued at weighted average cost.
            First In First Out (FIFO): The products are valued supposing those that enter the company first will also leave it first.
            """)
    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], string='Inventory Valuation',
        company_dependent=True, track_visibility='always', copy=True, required=True,
        help="""Manual: The accounting entries to value the inventory are not posted automatically.
            Automated: An accounting entry is automatically created to value the inventory when a product enters or leaves the company.
            """)
    property_stock_valuation_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account', track_visibility='always', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""When automated inventory valuation is enabled on a product, this account will hold the current value of the products.""", )

    property_stock_journal = fields.Many2one(
        'account.journal', 'Stock Journal', track_visibility='always', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0])]", check_company=True,
        help="When doing automated inventory valuation, this is the Accounting Journal in which entries will be automatically posted when stock moves are processed.")
    property_stock_account_input_categ_id = fields.Many2one(
        'account.account', 'Stock Input Account', track_visibility='always', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""Counterpart journal items for all incoming stock moves will be posted in this account, unless there is a specific valuation account
                    set on the source location. This is the default value for all products in this category. It can also directly be set on each product.""")
    property_stock_account_output_categ_id = fields.Many2one(
        'account.account', 'Stock Output Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", track_visibility='always',
        check_company=True,
        help="""When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account,
                    unless there is a specific valuation account set on the destination location. This is the default value for all products in this category.
                    It can also directly be set on each product.""")


class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = ['stock.warehouse', 'mail.thread']

    def _default_name(self):
        count = self.env['stock.warehouse'].with_context(active_test=False).search_count(
            [('company_id', '=', self.env.company.id)])
        return "%s - warehouse # %s" % (self.env.company.name, count + 1) if count else self.env.company.name

    name = fields.Char('Warehouse', index=True, track_visibility='always', required=True, default=_default_name)
    partner_id = fields.Many2one('res.partner', 'Address', default=lambda self: self.env.company.partner_id,
                                 track_visibility='always', check_company=True)


class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'mail.thread']

    name = fields.Char('Location Name', track_visibility='always', required=True)

    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Location Type',
        default='internal', index=True, required=True,
        tracking=True,
        help="* Vendor Location: Virtual location representing the source location for products coming from your vendors"
             "\n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products"
             "\n* Internal Location: Physical locations inside your own warehouses,"
             "\n* Customer Location: Virtual location representing the destination location for products sent to your customers"
             "\n* Inventory Loss: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)"
             "\n* Production: Virtual counterpart location for production operations: this location consumes the components and produces finished products"
             "\n* Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations")

    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade', check_company=True,
        track_visibility='always',
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        check_company=True, index=True, track_visibility='always',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=True)
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        check_company=True, index=True, track_visibility='always',
        domain="['&', ('product_tmpl_id', '=', product_tmpl_id), ('type', 'in', ['product', 'consu']),  '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If a product variant is defined the BOM is available only for this product.")

    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit')], 'BoM Type',
        default='normal', track_visibility='always', required=True)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def _get_default_date_planned_start(self):
        if self.env.context.get('default_date_deadline'):
            return fields.Datetime.to_datetime(self.env.context.get('default_date_deadline'))
        return datetime.datetime.now()

    lot_producing_id = fields.Many2one(
        'stock.production.lot', string='Lot/Serial Number', copy=False, track_visibility='always',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)

    date_planned_start = fields.Datetime(
        'Scheduled Date', copy=False, default=_get_default_date_planned_start,
        help="Date at which you plan to start the production.",
        index=True, required=True, track_visibility='always', )

    product_qty = fields.Float(
        'Quantity To Produce',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, required=True, tracking=True, track_visibility='always',
        states={'draft': [('readonly', False)]})

    user_id = fields.Many2one(
        'res.users', 'Responsible', default=lambda self: self.env.user, track_visibility='always',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        domain=lambda self: [('groups_id', 'in', self.env.ref('mrp.group_mrp_user').id)])

    qty_producing = fields.Float(string="Quantity Producing", track_visibility='always',
                                 digits='Product Unit of Measure', copy=False)


class PickingType(models.Model):
    _name = "stock.picking.type"
    _inherit = ['stock.picking.type', 'mail.thread']

    code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'),
                             ('internal', 'Internal Transfer'), ('mrp_operation', 'Manufacturing')],
                            'Type of Operation',
                            ondelete={'mrp_operation': 'cascade'}, required=True, track_visibility='always')

    default_location_src_id = fields.Many2one(
        'stock.location', 'Default Source Location',
        check_company=True, track_visibility='always',
        help="This is the default source location when you create a picking manually with this operation type. It is possible however to change it or that the routes put another location. If it is empty, it will check for the supplier location on the partner. ")

    default_location_dest_id = fields.Many2one(
        'stock.location', 'Default Destination Location',
        check_company=True, track_visibility='always',
        help="This is the default destination location when you create a picking manually with this operation type. It is possible however to change it or that the routes put another location. If it is empty, it will check for the customer location on the partner. ")
