# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import models, fields, _
from datetime import date
from odoo.exceptions import UserError
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_approved = fields.Boolean(string="Approved", default=False, readonly=True)

    def _get_forbidden_state_confirm(self):
        """
        Returns a set of states that cannot be confirmed
        It is written for the upgrading purposes, since a method with the same name and function was in v13.0
        """
        return set(['cancel', 'done'])

    def action_direct_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        # if self.env.user.has_group('sale.group_auto_done_setting'):
        #     self.action_done()
        return True

    def action_approve(self):
        self.is_approved = True

    def action_confirm(self):
        if self.is_approved == True:
            self.action_direct_confirm()
        else:
            if self.partner_id.is_due_date_block and self.partner_id.due_date_period > 0:
                res = super(SaleOrder, self).action_confirm()
                account_moves = self.env['account.move'].search(
                    [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice'),
                     ('state', '=', 'posted'), ('payment_state', '!=', 'paid'), ('payment_state', '!=', 'reversed')],
                    order='create_date ASC', limit=1)
                if account_moves:
                    today = date.today()
                    date1 = datetime.strptime(str(today), "%Y-%m-%d")
                    date2 = datetime.strptime(str(account_moves.invoice_date_due), "%Y-%m-%d")
                    date_difference = (date1 - date2).days
                    date_difference_int = int(date_difference)
                    if today > account_moves.invoice_date_due:
                        if self.partner_id.due_date_period < date_difference_int:
                            raise UserError(
                                "Following customer invoice {} due dates are lapse".format(account_moves.name))
                return res
            else:
                self.action_direct_confirm()
