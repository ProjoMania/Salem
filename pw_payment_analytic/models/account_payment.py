# -*- coding: utf-8 -*-

from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    # analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        write_off_line_vals = isinstance(write_off_line_vals, dict) and [write_off_line_vals]
        if not write_off_line_vals:
            return super()._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals,
                                                           force_balance=force_balance)
        for line_vals in write_off_line_vals:
            amount_currency = line_vals.get('amount', 0.0)
            if self.payment_type == 'inbound':
                amount_currency = line_vals.get('amount', 0.0)
                # Receive money.
            elif self.payment_type == 'outbound':
                # Send money.
                amount_currency = -line_vals.get('amount', 0.0)
            line_vals.pop('amount', 0.0)
            balance = self.currency_id._convert(
                from_amount=amount_currency,
                to_currency=self.env.company.currency_id,
                company=self.env.company.id,
                date=self.date,
            )
            line_vals.update({'amount_currency': amount_currency,
                              'balance': balance})
        result = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals, force_balance=force_balance)
        for move_line in result:
            if self.analytic_account_id:
                move_line.update({
                    'analytic_account_id': self.analytic_account_id.id,
                })
        print(result)
        return result

    def action_post(self):
        result = super(AccountPayment, self).action_post()
        for invoice_line in self.move_id.invoice_line_ids:
            if self.analytic_account_id:
                invoice_line.update({
                    'analytic_account_id': self.analytic_account_id.id
                })
        return result
