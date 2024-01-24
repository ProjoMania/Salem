# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_related_invoices(self):
        """Overridden from stock_account to return the customer invoices
        related to this stock move.
        """
        invoices = super()._get_related_invoices()
        line_invoices = self.mapped("sale_line_id.order_id.invoice_ids").filtered(
            lambda x: x.state == "posted"
        )
        invoices |= line_invoices
        return invoices