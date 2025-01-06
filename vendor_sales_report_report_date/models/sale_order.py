# -*- coding: utf-8 -*-
from odoo import models, fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    report_date = fields.Date('Report Date',compute='_compute_report_date',store=True)
    report_date1 = fields.Date('Report Date')
    is_report_date = fields.Boolean(string="Report Date" ,defualt=False)
    is_report_date1_invisible = fields.Boolean('Report Date',compute='_compute_is_report_date1_invisible')
    is_match_inv_date = fields.Boolean(string="Match Invoice date" ,defualt=False)

    @api.depends('invoice_ids','is_match_inv_date','is_report_date')
    def _compute_report_date(self):
        for rec in self:
            if rec.invoice_ids and rec.is_match_inv_date:
                rec.report_date= rec.invoice_ids.mapped('invoice_date')[0]
            elif rec.invoice_ids and rec.is_report_date:
                rec.report_date=rec.report_date1
                rec.report_date1=False
            else:
                rec.report_date=False

    @api.depends('is_match_inv_date','is_report_date')
    def _compute_is_report_date1_invisible(self):
            for rec in self:
                if rec.is_match_inv_date:
                    rec.is_report_date1_invisible=True
                else:
                    if rec.is_report_date and not rec.report_date:
                        rec.is_report_date1_invisible=False
                    else:
                        rec.is_report_date1_invisible=True

