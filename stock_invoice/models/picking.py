# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends('date_done', 'scheduled_date')
    def _get_delivery_date(self):
        for picking in self:
            if picking.state == 'done':
                delivery_date = picking.date_done.date()
            else:
                delivery_date = picking.scheduled_date.date()
            picking.delivery_date = delivery_date

    def _get_invoice_number(self):
        purchase_obj = self.env['purchase.order']
        sale_obj = self.env['sale.order']
        for picking in self:
            invoice_number = ''
            if picking.picking_type_code == 'incoming':
                purchase_order = purchase_obj.search([('name', '=', picking.origin)], limit=1)
                if purchase_order and purchase_order.invoice_ids:
                    invoice_number = purchase_order.invoice_ids[0].name
            elif picking.picking_type_code == 'outgoing':
                sale_order = sale_obj.search([('name', '=', picking.origin)], limit=1)
                if sale_order and sale_order.invoice_ids:
                    invoice_number = sale_order.invoice_ids[0].name
            picking.invoice_number = invoice_number

    def _get_invoice_id(self):
        purchase_obj = self.env['purchase.order']
        sale_obj = self.env['sale.order']
        for picking in self:
            invoice = False
            if picking.picking_type_code == 'incoming':
                purchase_order = purchase_obj.search([('name', '=', picking.origin)], limit=1)
                if purchase_order and purchase_order.invoice_ids:
                    invoice = purchase_order.invoice_ids[0].id
            elif picking.picking_type_code == 'outgoing':
                sale_order = sale_obj.search([('name', '=', picking.origin)], limit=1)
                if sale_order and sale_order.invoice_ids:
                    invoice = sale_order.invoice_ids[0].id
            picking.invoice_id = invoice

    delivery_date = fields.Date(string='Date', compute='_get_delivery_date')
    invoice_number = fields.Char(string='Invoice Number', compute='_get_invoice_number')
    invoice_id = fields.Many2one('account.move', string='Invoice', compute='_get_invoice_id')

    def get_current_user(self):
        return self.env.user

    def get_inventory_manager(self):
        return self.env.user

    def print_invoice(self):
        if self.invoice_id:
            return self.invoice_id.action_invoice_print()
