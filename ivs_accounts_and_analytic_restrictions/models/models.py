# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    user_ids = fields.Many2many('res.users', string="Users")

class AccountAccount(models.Model):
    _inherit = 'account.account'

    user_ids = fields.Many2many('res.users', string="Users")
