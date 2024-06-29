
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    def add_foc_product(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Add Product',
            'res_model': 'foc.product',
            'view_mode': 'tree',
            'domain': [('foc_product_id.id', '=', self.product_template_id.id)],
            'target': 'new',
        }
        return action