
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    product_category_ids = fields.Many2many('product.category', string='Product Category')
