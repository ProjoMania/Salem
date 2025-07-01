# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################


import datetime

from odoo import models, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain


class AgedReceivableCustomHandlerExtended(models.AbstractModel):
    _name = 'account.aged.receivable.report.handler.extended'
    _inherit = 'account.aged.partner.balance.report.handler'
    _description = 'Aged Receivable Custom Handler Extended'

    def open_journal_items(self, options, params):
        receivable_account_type = {'id': 'trade_receivable', 'name': _("Receivable"), 'selected': True}

        if 'account_type' in options:
            options['account_type'].append(receivable_account_type)
        else:
            options['account_type'] = [receivable_account_type]

        return super().open_journal_items(options, params)

    def _custom_unfold_all_batch_data_generator(self, report, options, lines_to_expand_by_function):
        # We only optimize the unfold all if the groupby value of the report has not been customized. Else, we'll just run the full computation
        if self.env.ref('account_reports.aged_receivable_line').groupby.replace(' ', '') == 'partner_id,id':
            return self._common_custom_unfold_all_batch_data_generator('asset_receivable', report, options, lines_to_expand_by_function)
        return {}

    def action_audit_cell(self, options, params):
        return super().aged_partner_balance_audit(options, params, 'sale')
