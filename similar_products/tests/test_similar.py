from odoo.tests import TransactionCase
from odoo.tests.common import SavepointCase
import logging


class SimilarProductTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls
        super(SimilarProductTestCase, cls).setUpClass()

        # create the data for each tests.
        product_record = [
            {'name': 'Office Chair A'},
            {'name': 'Office Chair B'},
            {'name': 'Drawer'}
        ]
        cls.products = cls.env['product.template'].create(product_record)

    def test_similar_products(self):
        for rec in self.products:
            logging.info(f'Test similar products: {rec.name}')
            rec.similar()
            logging.info(len(rec.similar_products))

        product = self.products.search([('name','=','Office Chair A')], limit=1)
        self.assertGreater(len(product.similar_products), 0)
