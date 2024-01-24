# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code == 'outgoing':
                if picking.move_line_ids_without_package:
                    for line in picking.move_line_ids_without_package:
                        if line.lot_id.product_qty < line.qty_done:
                            raise ValidationError(_('Lot "%s" (Available Qty: %s) has less qty than you are transferring %s !'
                                              %(line.lot_id.name, line.lot_id.product_qty, line.qty_done)))
        res = super(StockPicking, self).button_validate()
        return res
