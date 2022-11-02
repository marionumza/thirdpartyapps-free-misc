from odoo import _, api, fields, models
from odoo.osv.expression import OR


################################
# Product Product Default Code #
################################
class PRTProductCode(models.Model):
    _name = "prt.product.code"
    _description = "Internal Reference"

    """
    Store default codes for product in case
    they are changed and we need to find them to use later
    """
    _order = "name asc"

    name = fields.Char(string="Name", required=True, index=True)
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        ondelete="cascade",
        required=True,
    )
    is_default = fields.Boolean(string="Used as Default", compute="_compute_is_default")

    # -- If current code is default

    def _compute_is_default(self):
        for rec in self:
            if rec.name:
                if rec.product_id:
                    rec.is_default = (
                        True if rec.name == rec.product_id.default_code else False
                    )

    # -- Add code
    @api.model
    def add_code(self, code, product_id):
        """
        :param code: reference code
        :param product_id: product id
        :return: False or True

        """
        if not code:
            return False
        if not product_id:
            return False

        res = self.create(
            {
                "name": code,
                "product_id": product_id,
            }
        )
        return True if res else False

    # -- Button "Set as Default"
    def set_default(self):
        self.ensure_one()
        self.product_id.default_code = self.name

    # -- Create
    @api.model
    def create(self, vals):
        """
        Check if code already exist and prevent creating new one

        """
        product_id = vals.get("product_id", False)
        if not product_id:
            return False

        existing_code = self.search(
            [("product_id", "=", product_id), ("name", "=", vals.get("name"))]
        )
        if existing_code:
            res = existing_code[0]
        else:
            res = super(PRTProductCode, self).create(vals)

        # Check if code is set in the product
        if not res.product_id.default_code:
            res.product_id.default_code = res.name

        return res

    # -- Write
    def write(self, vals):
        """
        We do not want existing codes to be modified if duplicates exist

        """
        product_id = vals.get("product_id", False)
        product_ids = [product_id] if product_id else self.mapped("product_id").ids
        name = vals.get("name", False)
        names = [name] if name else self.mapped("name")

        existing_code = self.search(
            [("product_id", "in", product_ids), ("name", "in", names)]
        )
        if existing_code:
            return False

        return super(PRTProductCode, self).write(vals)

    def name_get(self):
        """ Change code name 'code [product.name]' """
        name = super(PRTProductCode, self).name_get()
        returned = []
        for record_id, _name in name:
            record = self.filtered(lambda r: r.id == record_id)
            if record:
                returned.append(
                    (record_id, "{} [{}]".format(record.name, record.product_id.name))
                )
        return returned


####################
# Product Template #
####################
class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Put here to be inherited by product.product!
    default_codes = fields.Char(
        string="Other References", related="product_variant_ids.default_code_ids.name"
    )
    default_code_tags = fields.Many2many(
        string="Other References",
        comodel_name="prt.product.code",
        compute="_compute_get_default_code_tags",
    )
    default_code_tag_count = fields.Integer(
        string="Other References", compute="_compute_default_code_tag_count"
    )

    # -- Count default code tags
    @api.depends("default_code_tags")
    def _compute_default_code_tag_count(self):
        for rec in self:
            rec.default_code_tag_count = len(rec.default_code_tags)

    # -- Get default code tags for template
    def _compute_get_default_code_tags(self):
        for rec in self:
            rec.default_code_tags = (
                rec.product_variant_ids.mapped("default_code_ids")
                .filtered(lambda x: x.name != rec.default_code)
                .ids
            )

    # -- Show product codes
    def show_codes(self):
        self.ensure_one()
        product_id = self.product_variant_id.id
        return {
            "name": _("Other Codes"),
            "views": [[False, "tree"], [False, "form"]],
            "res_model": "prt.product.code",
            "type": "ir.actions.act_window",
            "target": "current",
            "domain": [("product_id", "=", product_id)],
            "context": {"default_product_id": product_id, "create": True},
        }


###################
# Product Product #
###################
class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    default_code_ids = fields.One2many(
        string="Other References",
        comodel_name="prt.product.code",
        inverse_name="product_id",
    )
    default_codes = fields.Char(
        string="Other References", related="default_code_ids.name"
    )
    default_code_tags = fields.Many2many(
        string="Other References",
        comodel_name="prt.product.code",
        compute="_compute_get_default_code_tags",
    )
    default_code_tag_count = fields.Integer(
        string="Other References", compute="_compute_default_code_tag_count"
    )

    # -- Write
    """
    Save current code if code is changed
    """

    def write(self, vals):
        # Store current default code if changed
        if "default_code" in vals:
            for rec in self:
                if rec.default_code:
                    self.env["prt.product.code"].sudo().add_code(
                        rec.default_code, rec.id
                    )

        res = super(ProductProduct, self).write(vals)
        return res

    # -- Show product codes
    def show_codes(self):
        self.ensure_one()
        return {
            "name": _("Other Codes"),
            "views": [[False, "tree"], [False, "form"]],
            "res_model": "prt.product.code",
            "type": "ir.actions.act_window",
            "target": "current",
            "domain": [("product_id", "=", self.id)],
            "context": {"default_product_id": self.id, "create": True},
        }

    # -- Count default code tags
    @api.depends("default_code_tags")
    def _compute_default_code_tag_count(self):
        for rec in self:
            rec.default_code_tag_count = len(rec.default_code_tags)

    # -- Get default code tags for product
    def _compute_get_default_code_tags(self):
        for rec in self:
            rec.default_code_tags = rec.default_code_ids.filtered(
                lambda x: x.name != rec.default_code
            ).ids

    @api.model
    def _args_search_by_original_number(self, args):
        """
        Compute domain for search product by original number
        :param args: search domain args
        :return: new args domain
        """
        new_args = []
        for arg in args:
            if type(arg) == str:
                new_args.append(arg)
                continue
            field, cond, value = arg
            if field != "name":
                new_args.append(arg)
                continue
            line_ids = self.env["prt.product.code"].search([("name", cond, value)])
            if not line_ids:
                new_args.append(arg)
                continue
            original_number_args = [
                (
                    "default_code_ids",
                    "not in" if "!" in cond or "not" in cond else "in",
                    line_ids.ids,
                )
            ]
            new_args = OR([args, original_number_args])
        return new_args

    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        return super(ProductProduct, self)._search(
            args=self._args_search_by_original_number(args),
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
