# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import models, fields, api, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dr_has_discount = fields.Boolean(compute="_compute_dr_has_discount", search="_search_dr_has_discount")

    def _search_dr_has_discount(self, operator, value):
        pricelist_id = self._context.get('pricelist')
        if pricelist_id:
            all_product_data, discounted_product_ids = self._get_product_pricelist_data(pricelist_id)
            operator = 'in' if operator == '!=' else 'not in'
            return [('id', operator, discounted_product_ids)]
        return []

    def _need_catch_update(self, pricelist_id, catch_date):
        catch_date_obj = fields.Datetime.to_datetime(catch_date)
        item_ids_catch = self._pricelist_items_for_date(pricelist_id, catch_date)
        item_ids_now = self._pricelist_items_for_date(pricelist_id, fields.Datetime.to_string(fields.Datetime.now()))
        if set(item_ids_catch) != set(item_ids_now):
            return True

        if self.env['product.pricelist'].browse(pricelist_id).write_date > catch_date_obj:
            return True

        product_grouped_data = self.env['product.template'].read_group([('sale_ok', '=', True)], ['write_date:max'], ['sale_ok'])
        if product_grouped_data:
            product_date = product_grouped_data[0].get('write_date')
            if product_date > catch_date_obj:
                return True
        return False

    @api.model
    def _pricelist_items_for_date(self, pricelist_id, date):
        self.env['product.pricelist.item'].flush(['price', 'currency_id', 'company_id'])
        self.env.cr.execute(
            """ SELECT item.id FROM product_pricelist_item AS item
                WHERE (item.pricelist_id = %s) AND (item.date_start IS NULL OR item.date_start<=%s) AND (item.date_end IS NULL OR item.date_end>=%s)
            """, (pricelist_id, date, date))
        return [x[0] for x in self.env.cr.fetchall()]

    def _get_product_pricelist_data(self, pricelist_id):
        all_product_data, discounted_product_ids, catch_date = self._get_product_pricelist_cache(pricelist_id)
        need_catch_update = self._need_catch_update(pricelist_id, catch_date)
        if need_catch_update:
            self.clear_caches()
            all_product_data, discounted_product_ids, catch_date = self._get_product_pricelist_cache(pricelist_id)
        return all_product_data, discounted_product_ids

    @tools.ormcache('pricelist_id')
    def _get_product_pricelist_cache(self, pricelist_id):
        products = self.sudo().search([('sale_ok', '=', True)])    # Need sudo so all products are calculated
        pricelist = self.env['product.pricelist'].browse(pricelist_id)
        discounted_product_ids = []
        all_products_data = []
        for product in products:
            product_data = product._get_combination_info(pricelist=pricelist, only_template=True)
            all_products_data.append(self._dr_process_product_data(product_data, product))
            if product_data.get('has_discounted_price'):
                discounted_product_ids.append(product.id)
        return all_products_data, discounted_product_ids, fields.Datetime.to_string(fields.Datetime.now())

    def _dr_process_product_data(self, product_pricelist_data, product):
        return {'display_name': product_pricelist_data['display_name'], 'price': product_pricelist_data['price'], 'id': product_pricelist_data['product_template_id']}

    def _compute_dr_has_discount(self):
        for product in self:
            product.dr_has_discount = False

    def _get_product_category_count(self, domain=[]):
        tables, where_clause, where_clause_params = self._dr_prepare_query_parts(domain)
        query = """
            SELECT
                count(product_template.id),
                product_public_category.parent_path as path,
                product_public_category.parent_id as parent_id,
                product_public_category.id as product_public_category_id
            FROM product_public_category_product_template_rel
                JOIN product_template ON product_template.id = product_public_category_product_template_rel.product_template_id
                """ + tables + """
                RIGHT JOIN product_public_category ON product_public_category.id = product_public_category_product_template_rel.product_public_category_id
            WHERE """ + where_clause + """ or product_template.id is NULL
            GROUP BY product_public_category.id;
        """

        self.env.cr.execute(query, where_clause_params)
        query_res = self.env.cr.dictfetchall()

        result_count = dict([(line.get('product_public_category_id'), 0) for line in query_res])

        for line in query_res:
            for line2 in query_res:
                if line.get('parent_id'):
                    path_pattern = '/%s/' % line.get('product_public_category_id')
                    if path_pattern in line2.get('path'):
                        result_count[line.get('product_public_category_id')] += line2.get('count')
                else:
                    path_pattern = '%s/' % line.get('product_public_category_id')
                    if line2.get('path').startswith(path_pattern):
                        result_count[line.get('product_public_category_id')] += line2.get('count')

        return result_count

    def _get_product_attrib_count(self, attrib_values, domain=[]):
        tables, where_clause, where_clause_params = self._dr_prepare_query_parts(domain)

        query = """
            SELECT
                array_agg(product_template_attribute_line.product_tmpl_id) as product_tmpl_ids,
                min(product_template_attribute_line.attribute_id) as product_attrib_id,
                product_attribute_value.id
            FROM product_template_attribute_line
            JOIN product_attribute_value_product_template_attribute_line_rel
                ON product_attribute_value_product_template_attribute_line_rel.product_template_attribute_line_id = product_template_attribute_line.id
            JOIN product_attribute_value
                ON product_attribute_value.id = product_attribute_value_product_template_attribute_line_rel.product_attribute_value_id
            JOIN product_template ON product_template.id = product_template_attribute_line.product_tmpl_id
            """ + tables + """
            WHERE """ + where_clause + """ or product_template.id is NULL
            GROUP BY product_attribute_value.id
            ORDER BY product_attrib_id;
        """

        self.env.cr.execute(query, where_clause_params)
        query_res = self.env.cr.dictfetchall()

        result_count = {}

        if attrib_values:

            attrib_values_ids = [v[1] for v in attrib_values]
            attrib_ids = [v[0] for v in attrib_values]
            attrib_value_list = dict([(line.get('id'), line.get('product_tmpl_ids') or []) for line in query_res])

            # Attribute -> Attribute Vals map
            attrib_vals_map = {}
            for line in query_res:
                if not attrib_vals_map.get(line['product_attrib_id']):
                    attrib_vals_map[line['product_attrib_id']] = []
                attrib_vals_map[line['product_attrib_id']].append(line['id'])

            # Attribute -> active product list
            attrib_p_list = {}
            for line in query_res:

                value_id_1 = line.get('id')
                product_ids_1 = line.get('product_tmpl_ids') or []
                attrib_id_1 = line.get('product_attrib_id')

                if not attrib_p_list.get(attrib_id_1):
                    attrib_p_list[attrib_id_1] = set()

                if value_id_1 in attrib_values_ids:
                    attrib_p_list[attrib_id_1] = attrib_p_list[attrib_id_1] | set(product_ids_1)

            # Attribute -> final list
            attrib_product_list = {}
            for line in query_res:
                value_id_1 = line.get('id')
                product_ids_1 = line.get('product_tmpl_ids') or []
                attrib_id_1 = line.get('product_attrib_id')

                if not attrib_product_list.get(value_id_1):
                    attrib_product_list[value_id_1] = set(product_ids_1)

                for line_2 in query_res:
                    value_id_2 = line_2.get('id')
                    product_ids_2 = line_2.get('product_tmpl_ids') or []
                    attrib_id_2 = line_2.get('product_attrib_id')

                    if value_id_2 not in attrib_vals_map.get(attrib_id_1, []) and value_id_2 in attrib_values_ids:
                        attrib_product_list[value_id_1] = attrib_product_list[value_id_1] & attrib_p_list.get(attrib_id_2, set())

            result_count = dict([(val_id, len(product_ids)) for val_id, product_ids in attrib_product_list.items()])
        else:
            result_count = dict([(line.get('id'), len(line.get('product_tmpl_ids') or [])) for line in query_res])
        return result_count

    def _get_product_rating_count(self, domain=[]):
        tables, where_clause, where_clause_params = self._dr_prepare_query_parts(domain)
        query = """
            SELECT avg_rating, count(*) FROM (
                SELECT FLOOR(avg(rating)) as avg_rating, rating_rating.res_id FROM rating_rating JOIN product_template ON product_template.id = rating_rating.res_id """ + tables + """
                    WHERE (""" + where_clause + """) AND rating_rating.res_model = 'product.template' AND rating_rating.is_internal = False
            GROUP BY rating_rating.res_id) AS rating_count group by avg_rating; """

        self.env.cr.execute(query, where_clause_params)
        query_result = dict(self.env.cr.fetchall())
        total = 0
        ratings_result = {rating: 0 for rating in range(1, 6)}
        for result in range(5, 0, -1):
            total += query_result.get(result, 0)
            ratings_result[result] = total
        return ratings_result

    def _dr_prepare_query_parts(self, domain):
        query = self._where_calc(domain)
        self._apply_ir_rules(query)
        tables, where_clause, where_clause_params = query.get_sql()
        tables = tables.replace('"product_template"', ' ', 1)
        return tables, where_clause, where_clause_params

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if combination_info['product_id']:
            website = self.env['website'].get_current_website()
            # [TO-DO] startswith('theme_prime') is not a good way must need to find another way in next version
            # Note: kig-odoo
            theme_id = website.sudo().theme_id
            product_variant = self.env['product.product'].browse(combination_info['product_id'])
            if website and theme_id and theme_id.name.startswith('theme_prime'):
                IrUiView = self.env['ir.ui.view']
                combination_info['dr_extra_fields'] = IrUiView._render_template('theme_prime.product_extra_fields', values={'website': website, 'product_variant': product_variant, 'product': product_variant.product_tmpl_id})
                # Hide price per UoM feature for B2B mode
                if not website._dr_has_b2b_access():
                    combination_info['base_unit_price'] = 0
        return combination_info
