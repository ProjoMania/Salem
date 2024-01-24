# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    lot_state = fields.Selection(related='lot_id.state', string='Lot Status')
