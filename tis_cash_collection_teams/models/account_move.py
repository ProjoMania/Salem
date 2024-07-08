# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_is_zero, date_utils, email_split, email_re, html_escape, is_html_empty
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from contextlib import contextmanager
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings

# forbidden fields
INTEGRITY_HASH_MOVE_FIELDS = ('date', 'journal_id', 'company_id')
INTEGRITY_HASH_LINE_FIELDS = ('debit', 'credit', 'account_id', 'partner_id')


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):

        res = super(AccountMove, self)._post()

        if not self.env.su and not self.env.user.has_group(
                'account.group_account_invoice') and not self.env.user.has_group(
            'tis_cash_collection_teams.cash_collection_user_access'):
            raise AccessError(_("You don't have the access rights to post an invoice."))
        else:
            return res

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        current_user = self.env.user
        partner_ids = self.env['res.partner'].search([('cash_collection_team_id.member_ids', 'in', [self.env.user.id])])
        if not current_user.has_group('base.group_erp_manager') and current_user.has_group('tis_cash_collection_teams.cash_collection_user_access'):
            domain += [('partner_id', 'in', partner_ids.ids)]
        return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order,
                                       count_limit=count_limit)
