
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    max_qty = fields.Float(string="Maximum Quantity")
