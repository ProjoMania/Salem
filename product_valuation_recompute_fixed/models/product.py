from odoo import models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_recompute_valuation(self):
        StockValuationLayer = self.env['stock.valuation.layer']
        for product in self:
            layers = StockValuationLayer.search([('product_id', '=', product.id)])
            for layer in layers:
                # This will trigger recomputation of computed fields safely
                layer.write({'value': layer.value})
        return True
