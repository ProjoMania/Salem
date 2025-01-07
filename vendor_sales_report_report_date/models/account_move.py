# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    report_date = fields.Date(string='Report Date',compute='_compute_report_date')



    @api.depends('line_ids')
    def _compute_report_date(self):
        for rec in self:
            if rec.move_type == 'out_invoice':
                rec.report_date = rec.line_ids.sale_line_ids.order_id.report_date
            else:
                rec.report_date = False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    report_date = fields.Date(string='Report Date', related='move_id.report_date')
