# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models, _


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    invoicing_mode = fields.Selection([("standard", "Standard"), ("at_shipping", "At Shipping")], default="standard", string="Invoicing Mode")
