
from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"
    
    prefix = fields.Char("Prefix",help='Prefix used in sequence', default=lambda self: self.name  , required=True)