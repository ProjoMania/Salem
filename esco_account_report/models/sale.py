# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('date_order')
    def _get_order_date(self):
        for sale in self:
            date_order = False
            if sale.date_order:
                date_order = sale.date_order.date()
            sale.order_date = date_order

    order_date = fields.Date(string='Date Order', compute='_get_order_date')
