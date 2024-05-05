# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    # analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        write_off_line_vals = isinstance(write_off_line_vals, dict ) and [write_off_line_vals]
        for line_vals in write_off_line_vals:
            if line_vals.get('amount'):
                line_vals.update({
                    'amount_curreney': line_vals['amount']
                })
        result = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        for move_line in result:
            if self.analytic_account_id:
                move_line.update({
                    'analytic_account_id': self.analytic_account_id.id
                })
            # if self.analytic_tag_ids:
            #     move_line.update({
            #         'analytic_tag_ids':[(6, 0, self.analytic_tag_ids.ids)]
            #     })
        return result

    def action_post(self):
        result = super(AccountPayment, self).action_post()
        for invoice_line in self.move_id.invoice_line_ids:
            if self.analytic_account_id:
                invoice_line.update({
                    'analytic_account_id': self.analytic_account_id.id
                })
            # if self.analytic_tag_ids:
            #     invoice_line.update({
            #         'analytic_tag_ids':[(6, 0, self.analytic_tag_ids.ids)]
            #     })
        return result
