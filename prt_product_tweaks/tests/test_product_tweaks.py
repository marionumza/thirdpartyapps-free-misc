from odoo.tests import common


class TestPrtProductTweaks(common.TransactionCase):
    def setUp(self):
        super(TestPrtProductTweaks, self).setUp()

        ProductProduct = self.env["product.product"]
        ProductCategory = self.env["product.category"]
        PrtProductCode = self.env["prt.product.code"]

        self.product_cat_details = ProductCategory.create(
            {
                "name": "Details",
                "parent_id": self.ref("product.product_category_1"),
            }
        )

        self.product_pc_case = ProductProduct.create(
            {
                "name": "PC Case",
                "detailed_type": "consu",
                "categ_id": self.product_cat_details.id,
            }
        )

        self.pc_case_code_239 = PrtProductCode.create(
            {"name": "239-PC-C", "product_id": self.product_pc_case.id}
        )

        self.pc_case_code_235 = PrtProductCode.create(
            {"name": "235-PC-C", "product_id": self.product_pc_case.id}
        )

    def test_set_product_code_to_default(self):
        self.pc_case_code_235.set_default()
        self.assertEqual(self.pc_case_code_235.name, self.product_pc_case.default_code)

    def test_product_codes(self):
        pc_case_codes = self.pc_case_code_235.id and self.pc_case_code_239.id
        self.assertIn(pc_case_codes, self.product_pc_case.default_code_ids.ids)
