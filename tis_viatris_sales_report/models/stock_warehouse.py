# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.
from odoo import api, models,fields, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    hide_in_viatris_report = fields.Boolean(string="Hide in Viatris Report")
