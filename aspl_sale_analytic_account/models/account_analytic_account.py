# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    color = fields.Integer('Color Index', default=0)
