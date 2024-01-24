# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.
from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    customer_type = fields.Many2one('customer.type', string="Customer Type")


class CustomerType(models.Model):
    _name = "customer.type"

    name = fields.Char("Name")