# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    automated_sales_report = fields.Boolean(string="Send Automated Sales Report", default=False)
    area = fields.Char(string="Area")


