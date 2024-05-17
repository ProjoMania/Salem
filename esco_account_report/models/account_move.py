# -*- coding: utf-8 -*-

from odoo import models, fields, _

from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    picking_id = fields.Many2one('stock.picking', string='Picking')

    def get_pickings(self):
        pickings = []
        if self.invoice_origin:
            order = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
            if order.picking_ids:
                for picking in order.picking_ids:
                    pickings.append(picking)
        return pickings

    def action_invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('account.account_invoices').report_action(self)
        else:
            return self.env.ref('account.account_invoices_without_payment').report_action(self)
