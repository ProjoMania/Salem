# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_due_date_block = fields.Boolean(string='Due Date Block')
    due_date_period = fields.Integer(default=30)

