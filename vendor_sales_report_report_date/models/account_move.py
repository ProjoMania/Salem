# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    report_date = fields.Date(string='Report Date',compute='_compute_report_date')



    @api.depends('line_ids')
    def _compute_report_date(self):
        for rec in self:
            if rec.move_type == 'out_invoice' and rec.line_ids.sale_line_ids:
                order = rec.line_ids.sale_line_ids.order_id
                rec.report_date = order.report_date if not order.is_match_inv_date else rec.invoice_date
            else:
                rec.report_date = rec.invoice_date if rec.move_type == 'out_refund' else False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    report_date = fields.Date(string='Report Date', related='move_id.report_date')
