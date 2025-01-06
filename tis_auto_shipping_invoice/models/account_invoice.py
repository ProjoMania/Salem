# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _validate_invoice(self):
        return self.sudo().action_post()

    def call_js_remove_outstanding_partial(self, partial_id):
        self.js_remove_outstanding_partial(partial_id)
        return True

    def call_js_assign_outstanding_line(self, line_id):
        self.js_assign_outstanding_line(line_id)
        return True

    def button_draft(self):
        res = super().button_draft()
        return res or True

    def action_post(self):
        res = super().action_post()
        return res or True


# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"
#
#     def reconcile(self):
#         """ Reconcile the current move lines all together. """
#         return self.with_context(no_exchange_difference=True)._reconcile_plan([self])