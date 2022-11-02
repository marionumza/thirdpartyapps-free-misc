# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalAccount(CustomerPortal):
    
    def _document_check_access(self, model_name, document_id, access_token=None):
        document_sudo = super(PortalAccount, self)._document_check_access(model_name, document_id, access_token=access_token)
        if not request.env.user.partner_id.portal_document_access:
            raise AccessError(_("You are not allowed to access any documents."))
        return document_sudo