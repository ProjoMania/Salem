
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string="Credit Limit")
    sales_limit = fields.Float(string="Sales Limit")

    credit_sale_limit = fields.Boolean(string="Enable Credit-Sale Limitations")
