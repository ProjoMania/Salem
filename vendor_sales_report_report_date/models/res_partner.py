# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    auto_excluded = fields.Boolean(string="Auto Excluded From Sales Report", default=False)


