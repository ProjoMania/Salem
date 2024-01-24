# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime


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
