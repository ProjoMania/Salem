# -*- coding: utf-8 -*-
from odoo import models, fields,api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    report_date = fields.Date(string='Report Date',related='sale_id.report_date')

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    report_date = fields.Date(string='Report Date', related='picking_id.report_date')


class StockMove(models.Model):
        _inherit = 'stock.move'
        report_date = fields.Date(string='Report Date', related='picking_id.report_date')

