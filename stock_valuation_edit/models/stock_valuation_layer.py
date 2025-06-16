# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    unit_cost = fields.Monetary('Unit Value',readonly=False)


    def write(self, vals):
        if vals.get('unit_cost'):
            vals['value']=self.quantity  * vals['unit_cost']
        res = super(StockValuationLayer, self).write(vals)
        return res
