# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import models, api
from datetime import timedelta, date, datetime
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('invoice_date')
    def _onchange_invoicedate(self):
        if self.invoice_date:
            self.invoice_date_due = self.invoice_date + timedelta(days=self.partner_id.due_date_period)

    @api.onchange('partner_id')
    def _onchange_invoice(self):
        if self.invoice_date:
            self.invoice_date_due = self.invoice_date + timedelta(days=self.partner_id.due_date_period)

    def action_post(self):
        if self.partner_id.is_due_date_block and self.partner_id.due_date_period > 0:
            res = super(AccountMove, self).action_post()
            account_moves = self.search(
                [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice'),
                 ('state', '=', 'posted'), ('payment_state', '!=', 'paid')],
                order='create_date ASC', limit=1)
            if account_moves:
                today = date.today()
                date1 = datetime.strptime(str(today), "%Y-%m-%d")
                date2 = datetime.strptime(str(account_moves.invoice_date_due), "%Y-%m-%d")
                date_difference = (date1 - date2).days
                date_difference_int = int(date_difference)
                if today > account_moves.invoice_date_due:
                    if self.partner_id.due_date_period < date_difference_int:
                        raise UserError("Following customer invoice {} due dates are lapse".format(account_moves.name))
            return res
        else:
            return super(AccountMove, self).action_post()
