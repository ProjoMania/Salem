# from odoo import models, api

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     def action_print_invoice(self):
#         self.ensure_one()
#         if self.sale_id.invoice_ids:
#             invoice = self.sale_id.invoice_ids[0]  # Assume you want the first invoice, adjust as needed
#             return self.env.ref('account.account_invoices').report_action(invoice)
#         return False
from odoo import models, fields, api


class PrintInvoiceDelivery(models.TransientModel):
    _name = 'print.invoice.delivery'
    _description = 'Print Invoice from Delivery Order'

    def print_invoice(self):
        self.ensure_one()  # Ensure only one record is processed

        delivery_order = self.env.context.get('active_id')  # Get delivery order ID from context
        if not delivery_order:
            return {'warning': {'title': 'Error', 'message': 'No delivery order selected!'}}

        # Retrieve linked sale order and ensure it has an invoice
        sale_order = delivery_order.sale_id
        if not sale_order.invoice_ids:
            return {'warning': {'title': 'Error', 'message': 'No invoice found for this delivery order!'}}

        # Access the first invoice (assuming only one per delivery order)
        invoice = sale_order.invoice_ids[0]

        # Return a report action to print the invoice
        return invoice.action_report()