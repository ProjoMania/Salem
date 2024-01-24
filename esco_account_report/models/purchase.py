# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('date_planned')
    def _get_delivery_date(self):
        for purchase in self:
            delivery_date = False
            if purchase.date_planned:
                delivery_date = purchase.date_planned.date()
            purchase.delivery_date = delivery_date

    @api.depends('date_order')
    def _get_order_date(self):
        for purchase in self:
            date_order = False
            if purchase.date_order:
                date_order = purchase.date_order.date()
            purchase.order_date = date_order

    payment_type_id = fields.Many2one('payment.type', 'Payment Type')
    condition_term_id = fields.Many2one('condition.terms', 'Condition Terms')
    shipping_data_id = fields.Many2one('shipping.data', 'Shipping Data')
    delivery_date = fields.Date(string='Delivery Date', compute='_get_delivery_date')
    order_date = fields.Date(string='Date Order', compute='_get_order_date')
    validated_by_id = fields.Many2one('res.users', 'Validated By', copy=False)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.validated_by_id = self.env.user.id
        return True
