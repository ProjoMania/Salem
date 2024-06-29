
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    liquidation_id = fields.Many2one('stock.location', string='Liquidation Location')

