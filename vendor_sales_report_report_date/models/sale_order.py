# -*- coding: utf-8 -*-
from odoo import models, fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    report_date = fields.Date('Report Date')
    is_report_date = fields.Boolean(string="Report Date" ,defualt=False)
    is_match_inv_date = fields.Boolean(string="Match Invoice date" ,defualt=False)

    @api.onchange('is_report_date')
    def _onchange_is_report_date(self):
            if not self.is_report_date:
                if not self.is_match_inv_date:
                    pass
                else:
                    self.report_date=None

    @api.onchange('is_match_inv_date')
    def _onchange_is_match_inv_date(self):
        if self.is_match_inv_date:
            if self.invoice_ids.mapped('invoice_date'):
                self.report_date= self.invoice_ids.mapped('invoice_date')[0]
        else:
            self.report_date=False
