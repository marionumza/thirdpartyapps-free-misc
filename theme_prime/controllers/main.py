# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

import hashlib
import re
from datetime import timedelta, datetime

from odoo import http, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL, Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.tools import html_escape
from odoo.osv import expression


class ThemePrimeWebsiteSale(WebsiteSale):

    def _check_float(self, val):
        try:
            return float(val)
        except ValueError:
            pass
        return False

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True, search_price=True, search_rating=True):
        """ Overridden method used to apply extra filters.

            Extra parameters are added to generate skip some filters (Used for price range and attribute count)
            :param search_price: if false price domain will not be added,
        """
        domains = super(ThemePrimeWebsiteSale, self)._get_search_domain(search, category, attrib_values, search_in_description)

        # Hide out of stock
        if request.httprequest.args.get('hide_out_of_stock'):
            domains = expression.AND([domains, ['|', '|', ('type', '!=', 'product'), ('allow_out_of_stock_order', '=', True), '&', ('dr_free_qty', '>', 0), ('allow_out_of_stock_order', '=', False)]])

        # Tag
        tag = request.httprequest.args.getlist('tag')
        if tag:
            domains = expression.AND([domains, [('dr_tag_ids', 'in', [int(x) for x in tag])]])

        # Rating
        ratings = request.httprequest.args.getlist('rating')
        if ratings and search_rating:
            result = request.env['rating.rating'].sudo().read_group([('res_model', '=', 'product.template')], ['rating:avg'], groupby=['res_id'], lazy=False)
            rating_product_ids = []
            for rating in ratings:
                rating_product_ids.extend([item['res_id'] for item in result if item['rating'] >= int(rating)])
            if rating_product_ids:
                domains = expression.AND([domains, [('id', 'in', rating_product_ids)]])
            else:
                domains = expression.AND([domains, [('id', 'in', [])]])
        return domains

    def _prepare_product_values(self, product, category, search, **kwargs):
        res = super(ThemePrimeWebsiteSale, self)._prepare_product_values(product, category, search, **kwargs)
        ProductTemplate = request.env['product.template']
        res['prev_product_id'] = ProductTemplate.search([('website_sequence', '<', res['product'].website_sequence)] + request.website.website_domain(), limit=1, order='website_sequence desc')
        res['next_product_id'] = ProductTemplate.search([('website_sequence', '>', res['product'].website_sequence)] + request.website.website_domain(), limit=1, order='website_sequence')
        return res

    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        request.website = request.website.with_context(tp_shop_args=request.httprequest.args)
        response = super(ThemePrimeWebsiteSale, self).shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)
        ProductTemplate = request.env['product.template']
        theme_id = request.website.sudo().theme_id
        if theme_id and theme_id.name.startswith('theme_prime'):
            tags = request.env['dr.product.tags'].search(request.website.website_domain())

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split('-')] for v in attrib_list if v]
            attributes_ids = [v[0] for v in attrib_values]

            keep = QueryURL(
                '/shop',
                category=category and int(category),
                search=search,
                attrib=attrib_list,
                min_price=min_price,
                max_price=max_price,
                order=post.get('order'),
                tag=request.httprequest.args.getlist('tag'),
                hide_out_of_stock=request.httprequest.args.get('hide_out_of_stock'),
            )

            # Grid Sizing
            grid_style = request.website._get_dr_theme_config('json_grid_product')['style']
            if grid_style != '1':
                bins = []
                for product in response.qcontext.get('products'):
                    bins.append([{
                        'ribbon': product.website_ribbon_id,
                        'product': product,
                        'x': 1,
                        'y': 1
                    }])
                response.qcontext.update(
                    bins=bins
                )
            response.qcontext.update(grid_style=grid_style)
            fuzzy_search_term = response.qcontext.get('search') or search
            if request.website._get_dr_theme_config('json_shop_filters')['show_category_count']:
                domain = self._get_search_domain(fuzzy_search_term, None, attrib_values)
                get_category_count = ProductTemplate._get_product_category_count(domain=domain)
                response.qcontext.update(
                    get_category_count=get_category_count,
                )
            if request.website._get_dr_theme_config('json_shop_filters')['show_attrib_count'] or request.website._get_dr_theme_config('json_shop_filters')['hide_extra_attrib_value']:
                # Attributes
                domain = self._get_search_domain(fuzzy_search_term, category, [])
                get_attrib_count = ProductTemplate._get_product_attrib_count(attrib_values, domain=domain)
                response.qcontext.update(
                    get_attrib_count=get_attrib_count,
                )
                # Rating
                domain = self._get_search_domain(fuzzy_search_term, category, attrib_values, search_rating=False)
                response.qcontext.update(
                    get_ratings_count=ProductTemplate._get_product_rating_count(domain=domain),
                )

            selected_tags = [int(x) for x in request.httprequest.args.getlist('tag')]
            selected_ratings = [int(x) for x in request.httprequest.args.getlist('rating')]
            selected_hide_out_of_stock = request.httprequest.args.get('hide_out_of_stock')

            response.qcontext.update(
                tags=tags,
                keep=keep,
                attributes_ids=attributes_ids,
                selected_tags=selected_tags,
                selected_ratings=selected_ratings,
                selected_hide_out_of_stock=selected_hide_out_of_stock,
                is_activated_filter=response.qcontext.get('attrib_set') or request.httprequest.args.get('min_price') or request.httprequest.args.get('max_price') or selected_tags or selected_ratings or selected_hide_out_of_stock
            )
        return response

    @http.route(['/shop/cart'], type='http', auth='public', website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        res = super(ThemePrimeWebsiteSale, self).cart(access_token=access_token, revive=revive, **post)
        if post.get('type') == 'tp_cart_sidebar_request':
            order = request.website.sale_get_order()
            if order and order.state != 'draft':
                request.session['sale_order_id'] = None
            return request.render('theme_prime.cart_sidebar', {'order': order}, headers={'Cache-Control': 'no-cache'})
        return res

    @http.route('/theme_prime/search_sidebar', type='http', auth='public', website=True, sitemap=False)
    def search_sidebar(self, access_token=None, revive='', **post):
        return request.render('theme_prime.search_sidebar', headers={'Cache-Control': 'no-cache'})

    @http.route('/theme_prime/get_category_sidebar', type='http', auth='public', website=True, sitemap=False)
    def _get_category_sidebar(self, access_token=None, revive='', **post):
        return request.render('theme_prime.category_sidebar', headers={'Cache-Control': 'no-cache'})

    @http.route('/theme_prime/get_quick_view_html', type='json', auth='public', website=True)
    def get_quick_view_html(self, options, **kwargs):
        productID = options.get('productID')
        variantID = options.get('variantID')
        if variantID:
            productID = request.env['product.product'].browse(variantID).product_tmpl_id.id
        domain = expression.AND([request.website.sale_product_domain(), [('id', '=', productID)]])
        product = request.env['product.template'].search(domain, limit=1)

        # If moved to another website or delete
        if not product:
            return False

        values = self._prepare_product_values(product, category='', search='', **kwargs)
        Website = request.website
        result = Website.get_theme_prime_shop_config()
        values.update(result)
        if result.get('is_rating_active') and product.rating_count:
            values['rating'] = Website._get_theme_prime_rating_template(product.rating_avg, product.rating_count)
        values['d_url_root'] = request.httprequest.url_root[:-1]

        if options.get('mini'):
            values['auto_add_product'] = product.product_variant_count == 1
            return request.env["ir.ui.view"]._render_template('theme_prime.product_mini', values=values)

        if options.get('right_panel'):
            return request.env["ir.ui.view"]._render_template('theme_prime.tp_product_right_panel', values=values)
        return request.env["ir.ui.view"]._render_template('theme_prime.tp_product_quick_view', values=values)

    @http.route(['/tp_clear_cart'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def tp_clear_cart(self):
        sale_order = request.website.sale_get_order()
        [order_line.unlink() for order_line in sale_order.website_order_line] if sale_order else False
        return {}

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        response = super(ThemePrimeWebsiteSale, self).cart_update_json(product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, display=display, **kw)

        if kw.get('dr_cart_flow') and response:
            sale_order = request.website.sale_get_order(force_create=True)
            monetary_options = {'display_currency': sale_order.pricelist_id.currency_id}
            FieldMonetary = request.env['ir.qweb.field.monetary']
            cart_amount_html = FieldMonetary.value_to_html(sale_order.amount_total, monetary_options)
            product = request.env['product.product'].browse(int(product_id))
            response.update({
                'cart_quantity': sale_order.cart_quantity,
                'product_name': product.name,
                'product_id': int(product_id),
                'cart_amount_html': cart_amount_html,
                'accessory_product_ids': product.accessory_product_ids and product.accessory_product_ids.mapped('product_tmpl_id').ids or []
            })

        return response

    @http.route(['/theme_prime/reorder/<model("sale.order"):order>'], type='json', auth='user', website=True, sitemap=False)
    def tp_reorder(self, order, **kw):
        current_order = request.website.sale_get_order(force_create=1)
        current_order.sudo().order_line.unlink()
        response = False
        for line in order.sudo().website_order_line.filtered(lambda line: line.product_id.active):
            tmpl_id = line.product_id.product_tmpl_id.id
            domain = request.website.sale_product_domain()
            final_domain = expression.AND([[('website_published', '=', True), ('id', '=', tmpl_id)], domain])
            tmpl_rec = request.env['product.template'].search(final_domain)
            if tmpl_rec:
                response = self.cart_update_json(line.product_id.id, add_qty=line.product_uom_qty, dr_cart_flow='')
        return response


class DroggolWishlist(WebsiteSaleWishlist):
    @http.route('/theme_prime/wishlist_general', auth="public", type='json', website=True)
    def wishlist_general(self, product_id=False, **post):
        res = {}
        if product_id:
            res['wishlist_id'] = self.add_to_wishlist(product_id).id
        res.update({
            'products': request.env['product.wishlist'].with_context(display_default_code=False).current().mapped('product_id').ids,
            'name': request.env['product.product'].browse(product_id).name
        })
        return res


class ThemePrimeMainClass(http.Controller):

    # ----------------------------------------------------------
    # Helper methods
    # ----------------------------------------------------------

    def _get_products(self, domain=None, fields=[], limit=25, order=None):
        pricelist = request.website.get_current_pricelist()
        website_sale_domain = request.website.sale_product_domain()
        final_domain = expression.AND([website_sale_domain, domain])

        # bestseller is not a real field
        bestseller_ids, old_limit = [], limit
        if order == 'bestseller':
            bestseller_ids, limit, order = self._get_bestseller_products(old_limit)

        products = request.env['product.template'].with_context(pricelist=pricelist.id).search(final_domain, limit=limit, order=order)

        default_fields = ['id', 'name', 'website_url']
        fields = set(default_fields + fields)

        if bestseller_ids:
            bestseller_ids_filtered = set(bestseller_ids) & set(products.ids)
            bestseller_sorted_ids = [p_id for p_id in bestseller_ids if p_id in bestseller_ids_filtered]
            remain_products = set(products.ids) - set(bestseller_sorted_ids)
            final_product_ids = bestseller_sorted_ids + list(remain_products)
            products = request.env['product.template'].with_context(pricelist=pricelist.id).browse(final_product_ids[:old_limit])

        return self._prepare_product_data(products, fields)

    def _prepare_product_data(self, products, fields, options=None):

        options = options or {}
        pricelist = request.website.get_current_pricelist()
        price_public_visibility = request.website._dr_has_b2b_access()
        visibility_label = False
        showStockLabel = False

        if not price_public_visibility:
            visibility_label = self._get_tp_view_template('theme_prime.tp_b2b_price_label')

        extra_data = {'rating', 'offer_data', 'dr_stock_label', 'colors'} & set(fields)
        fields = list(set(fields) - extra_data)

        if 'dr_stock_label' in extra_data:
            showStockLabel = request.website._get_dr_theme_config('json_grid_product')['show_stock_label']
        currency_id = pricelist.currency_id

        result = products.read(fields)

        for res_product, product in zip(result, products):
            combination_info = product._get_combination_info(only_template=True)
            res_product.update(combination_info)
            price_info = self._get_computed_product_price(product, res_product, price_public_visibility, visibility_label, currency_id)
            res_product.update(price_info)
            res_product['product_variant_id'] = product._get_first_possible_variant_id()

            sha = hashlib.sha1(str(getattr(product, '__last_update')).encode('utf-8')).hexdigest()[0:7]
            # Images
            res_product['img_small'] = '/web/image/product.template/' + str(product.id) + '/image_256?unique=' + sha
            res_product['img_medium'] = '/web/image/product.template/' + str(product.id) + '/image_512?unique=' + sha
            res_product['img_large'] = '/web/image/product.template/' + str(product.id) + '/image_1024?unique=' + sha

            # short Description
            if 'description_sale' in fields:
                description = res_product.get('description_sale')
                res_product['short_description'] = description[:125] + '...' if description and len(description) > 125 else description or False
            # label and color
            if 'colors' in extra_data:
                res_product['colors'] = self._get_tp_view_template('theme_prime.tp_product_color_pills', {'product': product, 'limit': 4, 'no_label': True, '_classes': 'tp_snippet_for_card'})
            # label and color
            if 'dr_label_id' in fields and product.dr_label_id:
                res_product['label'] = product.dr_label_id
                res_product['label_id'] = product.dr_label_id.id
                res_product['label_template'] = self._get_tp_view_template('theme_prime.product_label', {'label': product.dr_label_id})
            if 'dr_stock_label' in extra_data and showStockLabel and product.dr_show_out_of_stock:
                res_product['dr_stock_label'] = self._get_tp_view_template('theme_prime.product_stock_label', {'product': product})
            # rating
            if 'offer_data' in extra_data:
                offer = product._get_product_pricelist_offer()
                if offer:
                    rule = offer.get('rule')
                    res_product['offer_data'] = {
                        'date_end': offer.get('date_end'),
                        'offer_msg': rule.dr_offer_msg,
                        'offer_finish_msg': rule.dr_offer_finish_msg
                    }

            if 'rating' in extra_data:
                res_product['rating'] = self._get_rating_template(product.rating_avg)
                res_product['rating_avg'] = product.rating_avg
            # images
            if 'product_variant_ids' in fields:
                res_product['images'] = product.product_variant_ids.ids
            # website_category
            if 'public_categ_ids' in fields and product.public_categ_ids:
                first_category = product.public_categ_ids[0]
                res_product['category_info'] = {
                    'name': first_category.name,
                    'id': first_category.id,
                    'website_url': '/shop/category/' + str(first_category.id),
                }
            # brand
            if 'dr_brand_value_id' in fields:
                res_product['brand_info'] = False
                if product.dr_brand_value_id:
                    res_product['brand_info'] = {
                        'name': product.dr_brand_value_id.name,
                        'id': product.dr_brand_value_id.id,
                    }

        return result

    def _get_computed_product_price(self, product, product_data, price_public_visibility, visibility_label, currency_id):
        FieldMonetary = request.env['ir.qweb.field.monetary']
        monetary_options = {'display_currency': currency_id}
        return {
            'price_raw': product_data['price'] if price_public_visibility else visibility_label,
            'list_price_raw': product_data['list_price'] if price_public_visibility else ' ',
            'price': FieldMonetary.value_to_html(product_data['price'], monetary_options) if price_public_visibility else visibility_label,
            'list_price': FieldMonetary.value_to_html(product_data['list_price'], monetary_options) if price_public_visibility else ' '
        }

    def _get_tp_view_template(self, tmpl, values={}):
        IrUiView = request.env['ir.ui.view']
        return IrUiView._render_template(tmpl, values=values)

    def _get_bestseller_products(self, old_limit):
        past_date = datetime.now() - timedelta(days=30)
        result = request.env['sale.report'].sudo().read_group([('date', '>', past_date), ('website_id', '=', request.website.id), ('state', 'in', ['sale', 'done'])], ['product_tmpl_id', 'product_uom_qty:sum'], ['product_tmpl_id'], orderby="product_uom_qty desc")
        return [product_line['product_tmpl_id'][0] for product_line in result], None if len(result) else old_limit, None

    def _get_shop_related_data(self, options):
        shop_data = {}
        if (options.get('shop_config_params')):
            shop_data['shop_config_params'] = request.website.get_theme_prime_shop_config()
        if (options.get('wishlist_enabled')) and shop_data.get('shop_config_params', {}).get('is_wishlist_active'):
            shop_data['wishlist_products'] = request.env['product.wishlist'].with_context(display_default_code=False).current().mapped('product_id').ids
        return shop_data

    def _get_rating_template(self, rating_avg, rating_count=False):
        return request.website._get_theme_prime_rating_template(rating_avg, rating_count)

    def _get_categories(self, domain=[], fields=['name', 'display_name', 'id'], limit=20, order=None):
        final_domain = expression.AND([request.website.website_domain(), domain])
        return request.env['product.public.category'].search_read(final_domain, fields=fields, limit=limit, order=order)

    def _get_products_for_top_categories(self, params):
        result = {}
        categoryIDs = params.get('categoryIDs')
        order = params.get('sortBy')
        operator = '='
        if params.get('includesChild'):
            operator = 'child_of'
        initial_domain = expression.AND([request.website.website_domain(), [('website_published', '=', True)]])
        for id in categoryIDs:
            domain = expression.AND([initial_domain, [['public_categ_ids', operator, id]]])
            products = self._get_products(domain, ['id'], 4, order)
            result[id] = [product['id'] for product in products]
        return result

    @http.route('/theme_prime/get_product_variant_img', type='json', auth='public', website=True, sitemap=False)
    def get_product_variant_img(self, attrID, **kw):
        ptav = request.env['product.template.attribute.value'].browse(attrID)
        if ptav.ptav_product_variant_ids:
            return f'/web/image/product.product/{ptav.ptav_product_variant_ids[0].id}/image_512/'
        return ''

    @http.route('/theme_prime/tp_search_read', type='json', auth='public', website=True, sitemap=False)
    def _tp_search_read(self, model, domain, fields=[], order=None, limit=20, extras={}, **post):
        if model == 'product.template':
            return self._get_products(domain, fields, limit, order)
        elif model == 'product.public.category':
            return self._get_categories(domain, fields, limit, order)
        elif model == 'product.attribute.value':
            if extras.get('brands'):
                brand_attributes = request.website._get_brand_attributes()
                domain = expression.AND([domain, [('attribute_id', 'in', brand_attributes.ids)]])
                return request.env[model].with_context(show_attribute=False).search_read(domain, fields=fields, limit=limit, order=order)
            return request.env[model].search_read(domain, fields=fields, limit=limit, order=order)
        elif model in ['dr.product.label', 'dr.product.tags']:
            return request.env[model].search_read(domain, fields=fields, limit=limit, order=order)

    @http.route('/theme_prime/tp_search_read/suggest', type='json', auth='public', website=True, sitemap=False)
    def _tp_search_read_suggest(self, model, domain, fields=[], order=None, extras={}, **post):
        if model == 'product.template':
            return self._get_products(domain, fields=fields, limit=5, order=order)
        elif model == 'product.public.category':
            return self._get_categories(domain, fields, limit=5, order=order)

    @http.route('/theme_prime/get_similar_products_sidebar', type='http', auth='public', website=True, sitemap=False)
    def _get_similar_products_sidebar(self, productID, **post):
        related_product = request.env['product.template'].browse(int(productID))
        shop_config = request.website.get_theme_prime_shop_config()
        return request.render('theme_prime.similar_products_sidebar', {'products': self._get_products([['id', 'in', related_product.alternative_product_ids.ids]], ['dr_label_id', 'public_categ_ids', 'rating']), 'is_rating_active': shop_config.get('is_rating_active')}, headers={'Cache-Control': 'no-cache'})

    @http.route('/theme_prime/get_tab_listing_products', type='json', auth='public', website=True)
    def get_tab_listing_products(self, domain=None, fields=[], options={}, limit=25, order=None, **kwargs):
        result = {}
        if options.get('categoryID', False):
            category_domain = [('id', '=', options.get('categoryID'))]
            category = self._get_categories(category_domain)
            if category:
                result['listing_category'] = category
                domain = expression.AND([domain, [('public_categ_ids', 'child_of', options.get('categoryID'))]])
        result['products'] = self._get_products(domain, fields, limit, order)
        result.update(self._get_shop_related_data(options))
        return result

    @http.route('/theme_prime/get_listing_products', type='json', auth='public', website=True)
    def get_listing_products(self, domain=None, fields=[], options={}, limit=5, **kwargs):
        result = {}
        # [TO-DO] even snippet don't allow manual selection it will set the attrs
        domain = None if options.get('mode') == 'manual' else domain
        if options.get('bestseller'):
            result['bestseller'] = self._get_products(domain, fields, limit, 'bestseller')
        if options.get('newArrived'):
            result['newArrived'] = self._get_products(domain, fields, limit, 'create_date desc')
        if options.get('discount'):
            if domain:
                domain = expression.AND([[("dr_has_discount", "!=", False)], domain])
            else:
                domain = [["dr_has_discount", "!=", False]]
            result['discount'] = self._get_products(domain, fields, limit)
        return result

    @http.route('/theme_prime/get_products_data', type='json', auth='public', website=True)
    def get_products_data(self, domain=None, fields=[], options={}, limit=25, order=None, **kwargs):
        result = {
            'products': self._get_products(domain, fields, limit, order),
        }
        result.update(self._get_shop_related_data(options))
        return result

    @http.route('/theme_prime/get_products_by_category', type='json', auth='public', website=True)
    def get_products_by_category(self, domain, fields=[], options={}, **kwargs):
        final_domain = expression.AND([[('website_published', '=', True)], domain])
        result = {
            'products': self._get_products(domain=final_domain, fields=fields, order=options.get('order', False), limit=options.get('limit', False)),
        }
        result.update(self._get_shop_related_data(options))
        if (options.get('get_categories')):
            # get category names for snippet
            domain = [('id', 'in', options.get('categoryIDs'))]
            result['categories'] = self._get_categories(domain)
        if (options.get('get_brands')):
            # get category names for snippet
            domain = [('id', 'in', options.get('categoryIDs'))]
            result['categories'] = request.website._get_brands(domain).read(['name', 'id'])
        return result

    @http.route('/theme_prime/get_top_categories', type='json', auth='public', website=True)
    def get_top_categories(self, options={}):
        params = options.get('params')
        result = []
        website_sale_domain = request.website.sale_product_domain()
        if params:
            categoryIDs = params.get('categoryIDs')
            if categoryIDs:
                domain = [('id', 'in', categoryIDs)]
                category_names = {i['id']: i['name'] for i in self._get_categories(domain)}
                # Update categoryIDs if already set category moved to other website
                categoryIDs = category_names.keys()
                params['categoryIDs'] = categoryIDs
                categories = self._get_products_for_top_categories(params)
                price_public_visibility = request.website._dr_has_b2b_access()
                for category_id in categoryIDs:
                    category_data = {}
                    product_ids = categories.get(category_id)
                    category_data['name'] = category_names.get(category_id)
                    category_data['id'] = category_id
                    category_data['website_url'] = '/shop/category/' + str(category_id)
                    category_data['productIDs'] = product_ids
                    final_domain = expression.AND([website_sale_domain, [('public_categ_ids', 'child_of', category_id)]])
                    products = self._get_products(domain=final_domain, fields=['price'], limit=1, order="list_price asc")
                    if len(products):
                        category_data['min_price'] = products[0].get('price')
                        category_data['price_public_visibility'] = price_public_visibility
                    result.append(category_data)
        return result

    @http.route(['/theme_prime/get_dialog_content'], type='json', website=True, auth="public")
    def get_dialog_content(self, res_id, res_model, fields, **post):
        return request.env[res_model].sudo().search_read([('id', '=', res_id)], fields=fields)

    @http.route('/theme_prime/save_website_config', type='json', auth='user', website=True)
    def save_website_config(self, configs, **post):
        request.env['dr.theme.config']._save_config(request.website.id, configs)
        return {'result': True}

    @http.route('/theme_prime/get_categories_info', type='json', auth='public', website=True)
    def get_categories_info(self, fields=[], options={}, **kwargs):
        categoryIDs = options.get('categoryIDs', [])
        fields = ['name', 'display_name', 'id'] + fields
        domain = expression.AND([request.website.website_domain(), [('id', 'in', categoryIDs)]])
        categories = request.env['product.public.category'].search(domain)
        result = categories.read(fields)
        if options.get('getCount', False):
            get_category_count = request.env['product.template']._get_product_category_count(domain=request.env['website'].sale_product_domain())
        for res_category, category in zip(result, categories):
            if 'dr_category_label_id' in fields and category.dr_category_label_id:
                category_label = category.dr_category_label_id
                res_category['category_lable_info'] = {
                    'id': category_label.id,
                    'name': category_label.name,
                    'background_color': category_label.background_color,
                    'text_color': category_label.text_color,
                }
            if options.get('getCount', False):
                res_category['count'] = get_category_count.get(category.id)
            res_category['website_url'] = '/shop/category/' + str(category.id)
            res_category['image_url'] = '/web/image?model=product.public.category&id=%d&field=image_512' % (category.id)
            res_category['cover_image'] = '/web/image?model=product.public.category&id=%d&field=dr_category_cover_image' % (category.id)
        return result

    @http.route('/theme_prime/get_brands', type='json', auth='public', website=True)
    def get_brands(self, fields=['id', 'name', 'attribute_id'], options={}):
        if options.get('categories'):
            domain = expression.AND([request.website.sale_product_domain(), [('public_categ_ids', 'child_of', options.get('categories'))]])
            brands = request.env['product.template'].search(domain).mapped('dr_brand_value_id')[:options.get('limit', 12)]
        else:
            brands = request.website._get_brands([], options.get('limit', 12))
            domain = request.env['website'].sale_product_domain()
        get_attrib_count = request.env['product.template']._get_product_attrib_count(attrib_values=[[brand.attribute_id.id, brand.id] for brand in brands], domain=domain)
        return [{**brand_data, 'product_count': get_attrib_count.get(brand_data['id'], 0)} for brand_data in brands.read(fields)]

    @http.route('/theme_prime/get_megamenu_categories', type='json', auth='public', website=True)
    def get_megamenu_categories(self, options, limit=5, fields=['name', 'id'], order='count', **kwargs):
        category_ids = request.env['product.public.category'].browse(options.get('categoryIDs', [])).exists().ids
        final_domain = expression.AND([request.website.website_domain(), [('parent_id', 'child_of', category_ids)]])
        categories = request.env['product.public.category'].search(final_domain, limit=None)

        all_categories = []
        all_category_count = request.env['product.template']._get_product_category_count(request.env['website'].sale_product_domain())
        for category in categories:
            all_categories.append({
                'id': category.id, 'name': category.name, 'parent_id': category.parent_id.id,
                'count': all_category_count.get(category['id'], 0),
                'website_url': '/shop/category/' + str(category.id),
                'image_url': '/web/image?model=product.public.category&id=%d&field=image_512' % (category.id),
                'cover_image': '/web/image?model=product.public.category&id=%d&field=dr_category_cover_image' % (category.id),
                'dr_category_icon': '/web/image?model=product.public.category&id=%d&field=dr_category_icon' % (category.id),
                'category_label_info': category.dr_category_label_id and {f: category.dr_category_label_id[f] for f in ['name', 'background_color', 'text_color']} or False,
            })

        parent_categories = filter(lambda category: category.get('id') in category_ids, all_categories)
        return [self._get_megamenu_child_categories(category_id, limit, all_categories, order) for category_id in parent_categories]

    def _get_megamenu_child_categories(self, parent_category, limit, all_categories, order):
        child_categories = [categ for categ in all_categories if categ.get('parent_id') == parent_category.get('id')]
        if not child_categories:
            return {'category': parent_category, 'child': []}
        if order == 'count' or not order:
            child_categories = sorted(child_categories, key=lambda category: category.get('count', 0), reverse=True)
        child_categories = child_categories[:limit]
        remain_limit = limit - len(child_categories)

        if remain_limit <= 0:
            return {'category': parent_category, 'child': child_categories}

        for child_category in child_categories:
            new_born_child = self._get_megamenu_child_categories(child_category, remain_limit, all_categories, order).get('child')
            child_categories.extend(new_born_child)
            remain_limit = limit - len(child_categories)
            if remain_limit <= 0:
                break
        return {'category': parent_category, 'child': child_categories}


class ThemeWebsite(Website):

    @http.route('/website/dr_search', type='json', auth="public", website=True)
    def dr_search(self, term, max_nb_chars, options, **kw):

        fuzzy_term, global_match = False, False
        search_config = request.website._get_dr_theme_config('json_product_search')
        has_formulate = self._dr_has_formulate(search_config)
        fuzzy_enabled = search_config.get('search_fuzzy')
        limit = max(min(search_config.get('search_limit'), 10), 5)
        search_types = ['products', 'categories', 'autocomplete', 'suggestions']
        results = {search_type: {'results': [], 'results_count': 0, 'parts': {}} for search_type in search_types}
        product_limit = max(min(search_config.get('search_max_product'), 5), 0)
        options = {'allowFuzzy': fuzzy_enabled, 'displayDescription': False, 'displayDetail': True, 'displayExtraLink': True, 'displayImage': True}
        if product_limit:
            results['products'] = self.autocomplete(search_type='products_only', term=term, order='name asc', limit=product_limit, options=options)
        product_fuzzy_term = results['products'].get('fuzzy_search')

        if search_config.get('search_category') and not has_formulate:
            results['categories'] = self.autocomplete(search_type='product_categories_only', term=term, order='sequence, name, id', limit=5, options=options)
            category_fuzzy_term = results['categories'].get('fuzzy_search')
            if fuzzy_enabled:
                empty_search = {'results': [], 'results_count': 0, 'parts': {}}
                if category_fuzzy_term == product_fuzzy_term:
                    fuzzy_term = product_fuzzy_term
                elif not category_fuzzy_term and results['categories'].get('results_count'):
                    results['products'], fuzzy_term = empty_search, False
                elif not product_fuzzy_term and results['products'].get('results_count'):
                    results['categories'], fuzzy_term = empty_search, False
                elif product_fuzzy_term and not category_fuzzy_term:   # category will be always empty based on above conditions
                    fuzzy_term = product_fuzzy_term
                elif category_fuzzy_term and not product_fuzzy_term:   # products will be always empty based on above conditions
                    fuzzy_term = category_fuzzy_term
                else:  # super rare case
                    all_results = self.autocomplete(search_type='products', term=term, order='sequence, name, id', limit=limit, options=options)
                    products_result = [res for res in all_results['results'] if res.get('_fa') == 'fa-shopping-cart']
                    category_result = [res for res in all_results['results'] if res.get('_fa') == 'fa-folder-o']
                    fuzzy_term = all_results.get('fuzzy_search')
                    results = {'products': {'results': products_result, 'results_count': len(products_result), 'parts': {}}, 'categories': {'results': category_result, 'results_count': len(category_result), 'parts': {}}}

        # suggestion search
        if search_config.get('search_attribute') or search_config.get('search_suggestion'):
            remain_limit = limit - min(product_limit, results['products'].get('results_count', 0))       # Odoo results_count returns count for full result (without limit)
            words = [i for i in term.split(' ') if i]   # split and filter spaces
            matchs, matched_dicts = False, {}
            for word in words:
                if matchs:
                    for match in matchs:
                        match_dict = matched_dicts[match]
                        if match_dict['remaining_words']:
                            match_dict['remaining_words'].append(word)
                        else:
                            unmatched_record_name = match_dict['unmatched_record_name']
                            regex_match = re.search(re.escape(word), unmatched_record_name, re.IGNORECASE)
                            if regex_match:
                                match_dict['matched_words'].append(word)
                                match_dict['unmatched_record_name'] = re.sub(re.escape(word), ' ', unmatched_record_name, flags=re.I)
                            else:
                                match_dict['remaining_words'].append(word)
                else:
                    matchs = self._match_attr_or_category(word)
                    if matchs:
                        for match in matchs:
                            matched_dicts[match] = match_dict = {'match': match, 'matched_words': [word], 'remaining_words': []}
                            match_dict['unmatched_record_name'] = re.sub(re.escape(match_dict['matched_words'][0]), ' ', match.ds_name, flags=re.I)

            match_list = list(matched_dicts.values())
            match_list.sort(key=lambda m: len(m['matched_words']), reverse=True)
            autocomplete_result = []

            for match_dict in match_list:
                autocomplete_data = []
                if match_dict['remaining_words']:
                    autocomplete_data = self._get_autocomplete_data(match_dict, remain_limit, search_config)
                elif not search_config.get('search_category') and match_dict['match']._name == 'product.public.category':
                    autocomplete_data = [self.generate_result_dict(match_dict['match'], False, match_dict['matched_words'], '')]
                if not match_dict['remaining_words']:
                    # if no remaining_words that means full data matched with record so suggestions become autocomplete
                    autocomplete_data += self._get_suggestions_data(match_dict, autocomplete_result, remain_limit, search_config, ignore_config=True)
                remain_limit -= len(autocomplete_data)
                autocomplete_result.extend(autocomplete_data)
                if not remain_limit:
                    break

            suggestions_result = []
            for match_dict in match_list:
                suggestions_data = self._get_suggestions_data(match_dict, autocomplete_result, min(remain_limit, 5), search_config)
                remain_limit -= len(suggestions_data)
                suggestions_result.extend(suggestions_data)
                if not remain_limit:
                    break

            results['autocomplete'] = {'results': autocomplete_result, 'results_count': len(autocomplete_result), "parts": {"name": True, "website_url": True}}
            results['suggestions'] = {'results': suggestions_result, 'results_count': len(suggestions_result), "parts": {"name": True, "website_url": True}}

            global_match = False
            if matchs and len(matchs) == 1 and (results['autocomplete'].get('results_count') or results['suggestions'].get('results_count')):
                if matchs._name == 'product.public.category':
                    fixed_str = _('View all products with category')
                    global_match = {'name': f'{fixed_str} <b class="text-primary">{matchs.ds_name}</b>', 'website_url': f'/shop?category={matchs.id}'}
                else:
                    fixed_str = _('View all products with')
                    global_match = {'name': f'{fixed_str} {matchs.attribute_id.name.lower()} <b class="text-primary">{matchs.ds_name}</b>', 'website_url': f'/shop?&attrib={matchs.attribute_id.id}-{matchs.id}'}

        return {**results, 'fuzzy_search': fuzzy_term, 'results': [], 'global_match': global_match,
                'result_length': sum([results.get(r_type, {}).get('results_count', 0) for r_type in search_types]),
                }

    def _get_autocomplete_data(self, match_dict, remain_limit, search_config):
        match, remaining_words, matched_words = match_dict['match'], match_dict['remaining_words'], match_dict['matched_words']
        results = []
        if search_config.get('search_attribute') and remaining_words and match:
            for related_match, word in self.match_remaining_words(match, remaining_words):
                results.append(self.generate_result_dict(match, related_match, matched_words, word))
                matched_words.append(word)
                if len(results) >= remain_limit:
                    break
        return results

    def _get_suggestions_data(self, match_dict, autocomplete_data, remain_limit, search_config, ignore_config=False):
        results = []
        match, matched_words = match_dict['match'], match_dict['matched_words']
        if (search_config.get('search_suggestion') or ignore_config) and remain_limit > 0:
            if match._name == 'product.public.category':
                for related_match in self._category_counterpart_iterator(match, search_type=['auto_suggestion']):
                    term = self.generate_result_dict(match, related_match, matched_words)
                    if not self.is_search_added(autocomplete_data, results, term):
                        results.append(term)
                    if len(results) >= remain_limit:
                        break
            else:
                domain = request.website.sale_product_domain() + [('attribute_line_ids.value_ids', 'in', match.ids)]
                all_related_records = request.env['product.template'].with_context(bin_size=True).search(domain).mapped('public_categ_ids')
                for related_match in all_related_records:
                    term = self.generate_result_dict(match, related_match, matched_words)
                    if not self.is_search_added(autocomplete_data, results, term):
                        results.append(term)
                    if len(results) >= remain_limit:
                        break
        return results

    def _match_attr_or_category(self, term, return_on_match=True):
        result = self._match_category(term)
        if not result:
            result = self._match_attr(term)
        return result

    def _match_category(self, term):
        ProductCategory = request.env['product.public.category']
        matched_categories = ProductCategory.search([('ds_name', 'ilike', term)] + request.website.website_domain())
        return matched_categories

    def _match_attr(self, term):
        all_active_attributes = self._website_active_attributes()
        matched_values = request.env['product.attribute.value']
        if all_active_attributes:
            matched_values = matched_values.search([('ds_name', 'ilike', term), ('attribute_id', 'in', all_active_attributes.ids)])
        return matched_values

    def _website_active_attributes(self):
        all_products = request.env['product.template'].with_context(bin_size=True).search(request.website.sale_product_domain())
        return request.env['product.attribute'].search([
            ('product_tmpl_ids', 'in', all_products.ids), ('visibility', '=', 'visible'), ('dr_search_suggestion', '!=', False)
        ])

    def match_remaining_words(self, match, remaining_words):
        if match._name == 'product.public.category':
            for word in remaining_words:
                for attribute_value in self._category_counterpart_iterator(match):
                    regex_match = re.search(re.escape(word), attribute_value.ds_name, re.IGNORECASE)
                    if regex_match:
                        yield attribute_value, word

        if match._name == 'product.attribute.value':
            domain = request.website.sale_product_domain() + [('attribute_line_ids.value_ids', 'in', match.ids)]
            categories = request.env['product.template'].with_context(bin_size=True).search(domain).mapped('public_categ_ids')
            for word in remaining_words:
                for category in categories:
                    regex_match = re.search(re.escape(word), category.ds_name, re.IGNORECASE)
                    if regex_match:
                        yield category, word

    def _category_counterpart_iterator(self, category, search_type=['auto_suggestion', 'auto']):
        attribute_values = category.mapped('product_tmpl_ids.attribute_line_ids').filtered(lambda line: line.attribute_id.dr_search_suggestion in search_type).mapped('value_ids')
        for value in attribute_values:
            yield value

        # Child category
        child_categories = request.env['product.public.category'].search([('parent_id', 'child_of', category.id)]) - category
        child_attribute_values = child_categories.mapped('product_tmpl_ids.attribute_line_ids').filtered(lambda line: line.attribute_id.dr_search_suggestion in search_type).mapped('value_ids')   # plus to maintain order
        for value in child_attribute_values:
            if value not in attribute_values:
                yield value

    def generate_result_dict(self, primary_match, secondary_match, matched_words, word=False):
        category, attribute = (primary_match, secondary_match) if primary_match._name == 'product.public.category' else (secondary_match, primary_match)
        attribute_str = f"&attrib={attribute.attribute_id.id}-{attribute.id}" if attribute else ''  # just for category
        return {
            'name': self.format_result(matched_words + (word and [word] or []), f"{primary_match.ds_name} {secondary_match and secondary_match.ds_name or ''}"),
            'website_url': f"/shop?category={category.id}{attribute_str}"
        }

    def format_result(self, matched_words, value):
        pattern = '|'.join(map(re.escape, matched_words))
        parts = re.split(f'({pattern})', value, flags=re.IGNORECASE)
        if len(parts) > 1:
            value = request.env['ir.ui.view'].sudo()._render_template("website.search_text_with_highlight", {'parts': parts})
            html_val = request.env[('ir.qweb.field.html')].value_to_html(value, {'template_options': {}})
            return html_escape(html_val)
        return False

    def is_search_added(self, autocomplete_result, suggestions_results, new_term):
        auto_found = len([term for term in autocomplete_result if new_term['website_url'] == term['website_url']])
        sugg_found = len([term for term in suggestions_results if new_term['website_url'] == term['website_url']])
        return auto_found + sugg_found

    def _dr_has_formulate(self, search_config):    # for performance
        if search_config.get('search_attribute') or search_config.get('search_suggestion'):
            formulate_category = request.env['product.public.category'].search(([('dr_search_formulate', '=', True)] + request.website.website_domain()), limit=1)
            if formulate_category:
                request.context = dict(request.context, dr_formulate=True)
            return len(formulate_category)
        return False
