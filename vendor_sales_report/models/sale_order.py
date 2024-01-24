# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_type = fields.Char('Sales Type')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_returned = fields.Float(

        string="Returned Qty"
    )