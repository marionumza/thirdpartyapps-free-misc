# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii
from datetime import date

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
import logging

logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        if request.env.user.partner_id.parent_id:
            partner_id = request.env.user.partner_id.parent_id
        else:
            partner_id = request.env.user.partner_id
        ResCurrency = request.env['res.currency']

        domain = [
            ('partner_id', '=', partner_id.id)
        ]
        SaleOrder = request.env['sale.order']
        Payment = request.env['account.payment']
        DebtLine = request.env['account.debt.line']

        quotation_count = SaleOrder.sudo().search_count([
            ('partner_id', '=', partner_id.id),
            ('state', 'in', ['draft','sent', 'cancel'])
        ])
        order_count = SaleOrder.sudo().search_count([
            ('partner_id', '=', partner_id.id),
            ('state', 'in', ['sale', 'done'])
        ])
        debt_line_count = DebtLine.sudo().search_count([
            ('partner_id', '=', partner_id.id),
        ])

        values['quotation_count'] = quotation_count
        values['order_count'] = order_count
        values['debt_line_count'] = debt_line_count

        logger.warning('[DEBUG #1] values %s'%(values))
        return values


    @http.route(['/my/debt_lines', '/my/debt_lines/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_debt_lines(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        DebtLine = request.env['account.debt.line']
        if request.env.user.partner_id.parent_id:
            partner_id = request.env.user.partner_id.parent_id
        else:
            partner_id = request.env.user.partner_id

        domain = [
            ('partner_id', '=', partner_id.id),
        ]

        searchbar_sortings = {
            'name': {'label': _('date'), 'order': 'name'},
        }
        # default sortby order
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['label']

        #archive_groups = self.sudo()._get_archive_groups('account.debt.line', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        debt_line_count = DebtLine.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/debt_line",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=debt_line_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        debt_lines = DebtLine.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_debt_lines_history'] = debt_lines.ids[:100]

        values.update({
            'date': date_begin,
            'debt_lines': debt_lines.sudo(),
            'page_name': 'debt',
            'pager': pager,
            #'archive_groups': archive_groups,
            'default_url': '/my/debt_lines',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        logger.warning('[DEBUG #5] values %s'%(values))
        return request.render("account_debt_portal.portal_my_debt_lines", values)


