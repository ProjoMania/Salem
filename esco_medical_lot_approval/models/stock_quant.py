# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _order = 'life_date asc, id asc'

    @api.depends('lot_id.life_date', 'lot_id.life_date_format')
    def _compute_life_date(self):
        for quant in self:
            quant.life_date = quant.lot_id.life_date
            quant.life_date_format = quant.lot_id.life_date_format

    removal_date = fields.Date(related='lot_id.removal_date', store=True, readonly=False)
    # expiration_date = fields.Datetime(related='lot_id.expiration_date', store=True, readonly=False)
    life_date = fields.Date(compute='_compute_life_date', string='End of Life Date', store=True)
    life_date_format = fields.Char(compute='_compute_life_date', string='End of Life Date')

    @api.model
    def _get_removal_strategy_order(self, removal_strategy):
        print(removal_strategy)
        if removal_strategy == 'fifo':
            return 'in_date ASC, id'
        elif removal_strategy == 'lifo':
            return 'in_date DESC, id DESC'
        elif removal_strategy == 'closest':
            return 'location_id ASC, id DESC'
        elif removal_strategy == 'fefo':
            return 'life_date, in_date, id'
        raise UserError(_('Removal strategy %s not implemented.') % (removal_strategy,))
