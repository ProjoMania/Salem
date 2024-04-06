# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()
        for picking in self:
            if picking._invoice_at_shipping():
                picking._invoicing_at_shipping()
        return res

    def _invoice_at_shipping(self):
        """Check if picking must be invoiced at shipping."""
        self.ensure_one()
        return (
            self.picking_type_code == "outgoing"
            and self.company_id.invoicing_mode == "at_shipping" and self.location_id.warehouse_id.invoicing_mode == "at_shipping"
        )

    def _invoicing_at_shipping(self):
        self.ensure_one()
        sales = self.env["sale.order"].browse()
        # Filter out non invoicable sales order
        for sale in self._get_sales_order_to_invoice():
            if sale._get_invoiceable_lines():
                sales |= sale
        invoices = _("Nothing to invoice.")
        if sales:
            invoices = self.env["account.move"].browse()
            invoices |= sales._create_invoices(grouped=False)
            for invoice in invoices:
                invoice._validate_invoice()
        return invoices or _("Nothing to invoice.")

    def _get_sales_order_to_invoice(self):
        return self.mapped("move_ids.sale_line_id.order_id").filtered(
            lambda r: r._get_invoiceable_lines()
        )

