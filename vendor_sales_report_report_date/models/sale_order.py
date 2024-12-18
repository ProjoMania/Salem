# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    report_date = fields.Date('Report Date')
