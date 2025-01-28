# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    quarantine_product_domain = fields.Json(string="Quarantine Product Domain", compute="_compute_quarantine_product_domain")

    @api.depends('lot_id', 'picking_type_id')
    def _compute_quarantine_product_domain(self):
        for line in self:
            domain = [('product_id', '=', line.product_id.id), ('location_id', 'child_of', line.picking_id.location_id.id)]
            if line.picking_type_id.allow_quarantine_delivery:
                line.quarantine_product_domain = domain
            else:
                line.quarantine_product_domain = domain + [('lot_id.state', '=', 'released')]

    def button_validate(self):
        res = super().button_validate()
        for line in self:
            if not line.picking_id.picking_type_id.allow_quarantine_delivery:
                if line.lot_id and line.lot_state != 'approved':
                    _logger.info(f"Quarantine product should be released !")
                    raise ValidationError(_(f'Quarantine product should be released!'))
        return res


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    allow_quarantine_delivery = fields.Boolean(string="Allow Quarantine", default=True)
