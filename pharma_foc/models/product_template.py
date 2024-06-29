
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    foc_product_ids = fields.One2many('foc.product', 'foc_product_id', string="FOC Product")
    