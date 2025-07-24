from odoo import models, api, _
from odoo.exceptions import UserError

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    @api.onchange('scrap_qty')
    def _onchange_scrap_qty_integer(self):
        for rec in self:
            if rec.scrap_qty and rec.scrap_qty != int(rec.scrap_qty):
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _('Scrap Quantity must be an integer value (e.g., 2 or 2.00). Decimals are not allowed: %s') % rec.scrap_qty
                    }
                }