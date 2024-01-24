# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models, _


class Company(models.Model):
    _inherit = 'res.company'

    invoicing_mode = fields.Selection([("standard", "Standard"), ("at_shipping", "At Shipping")], default="standard", string="Invoicing Mode")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoicing_mode = fields.Selection([("standard", "Standard"), ("at_shipping", "At Shipping")], string="Invoicing Mode", related='company_id.invoicing_mode', store=True)














