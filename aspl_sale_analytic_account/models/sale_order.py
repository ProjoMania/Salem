# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    color_anytic = fields.Integer(related="analytic_id.color")

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.analytic_id:
            res['analytic_account_id'] = self.analytic_id.id
        return res
