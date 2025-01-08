# -*- coding: utf-8 -*-
from odoo import models, fields,api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    report_date = fields.Date('Report Date',compute='_compute_report_date',store=False)
    report_date1 = fields.Date('Report Date')
    is_report_date = fields.Boolean(string="Report Date" ,defualt=False)
    is_report_date1_invisible = fields.Boolean('Report Date',compute='_compute_is_report_date1_invisible')
    is_match_inv_date = fields.Boolean(string="Match Invoice date" ,defualt=False)
    
    @api.constrains('is_match_inv_date','is_report_date')
    def _check_is_match_inv_date(self):
        if self.is_match_inv_date and self.is_report_date:
            raise ValidationError("You can't select both Match Invoice Date and Report Date")
        if not self.is_match_inv_date and not self.is_report_date:
            raise ValidationError("You must select either Match Invoice Date or Report Date")

    @api.depends('invoice_ids','is_match_inv_date','is_report_date')
    def _compute_report_date(self):
        for rec in self:
            if rec.invoice_ids and rec.is_match_inv_date and not rec.report_date1:
                rec.report_date= rec.invoice_ids.filtered(lambda o: o.move_type == 'out_invoice').mapped('invoice_date')[0]
            elif rec.invoice_ids and rec.is_report_date and not rec.report_date:
                rec.report_date = rec.report_date1
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

