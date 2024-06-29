# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FOCProduct(models.Model):
    _name = 'foc.product'
    _description = 'FOC Products'

    product_id = fields.Many2one('product.template', String="Product")
    percentage = fields.Float(String="%")
    foc_product_id = fields.Many2one('product.template', readonly=True)
    
    def add_product(self):
        if self._context.get('active_model') == 'sale.order.line':
            active_id = self.env['sale.order.line'].browse(self._context.get('active_id'))
            foc_product_qty = 0.0
            foc_product_qty = 1 if self.percentage == 0.0 else int(active_id.product_uom_qty * (self.percentage/100))
            vals = {
                'product_id': self.product_id.product_variant_id.id,
                'name': self.product_id.name,
                'product_uom_qty': foc_product_qty,
                'price_unit': 0,
                'order_id': active_id.order_id.id,
            }
            sale_order_line_id = self.env['sale.order.line'].create(vals)
        elif self._context.get('active_model') == 'visit.lines':
            active_visit_id = self.env['visit.lines'].browse(self._context.get('active_id'))
            foc_product_qty = 1
            values = {
                'product_id': self.product_id.product_variant_id.id,
                'visit_id': active_visit_id.visit_id.id,
                'amount': 0,
                'qty': foc_product_qty,
            }
            visit_lines = self.env['visit.lines'].create(values)