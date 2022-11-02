###################################################################################
# 
#    Copyright (C) Cetmix OÜ
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerCategory(common.TransactionCase):
    def setUp(self):
        super(TestPartnerCategory, self).setUp()
        ResPartnerCategory = self.env["res.partner.category"]
        ResPartner = self.env["res.partner"]

        self.res_partner_test_1 = ResPartner.create({"name": "Test Partner #1"})

        self.res_partner_test_2 = ResPartner.create({"name": "Test Partner #2"})

        self.res_partner_category_test_1 = ResPartnerCategory.create(
            {
                "name": "Test Category",
            }
        )

    def test_onchange_auto_subscribe(self):
        self.res_partner_category_test_1.write({"auto_subscribe": True})
        with self.assertRaises(UserError):
            self.res_partner_category_test_1.onchange_auto_subscribe()
        self.res_partner_category_test_1.write(
            {
                "auto_subscribe": False,
                "auto_unsubscribe": True,
            }
        )
        with self.assertRaises(UserError):
            self.res_partner_category_test_1.onchange_auto_subscribe()
        self.res_partner_category_test_1.write(
            {
                "auto_subscribe": True,
                "auto_unsubscribe": True,
            }
        )
        with self.assertRaises(UserError):
            self.res_partner_category_test_1.onchange_auto_subscribe()

    def test_compute_partner_count(self):
        self.res_partner_category_test_1._compute_partner_count()
        self.assertEqual(self.res_partner_category_test_1.partner_count, 0)
        self.res_partner_category_test_1.write(
            {
                "partner_ids": [
                    (4, self.res_partner_test_1.id),
                    (4, self.res_partner_test_2.id),
                ]
            }
        )
        self.assertEqual(self.res_partner_category_test_1.partner_count, 2)

    def test_name_get(self):
        self.res_partner_category_test_1.write(
            {
                "partner_ids": [
                    (4, self.res_partner_test_1.id),
                    (4, self.res_partner_test_2.id),
                ]
            }
        )

        category = self.res_partner_category_test_1.id
        reference_result_without_context = [(category, "Test Category")]
        reference_result_with_context = [(category, "Test Category (2)")]

        result = self.res_partner_category_test_1.name_get()
        self.assertEqual(result, reference_result_without_context)
        result = self.res_partner_category_test_1.with_context(
            partner_count_display=True
        ).name_get()
        self.assertEqual(result, reference_result_with_context)
