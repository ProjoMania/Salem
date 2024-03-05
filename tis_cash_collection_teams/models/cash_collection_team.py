# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import api, fields, models
from datetime import date


class CashCollectionTeams(models.Model):
    _name = "cash.collection.teams"
    _description = "Cash Collection Teams"
    _rec_name = 'name'
    _order = 'id DESC'

    name = fields.Char('Cash Collection Team', required=True, translate=True)
    user_id = fields.Many2one('res.users', string='Team Manager', check_company=True)
    member_ids = fields.Many2many('res.users', string='Cash Collector Users', help="Users assigned to this team.")
    company_id = fields.Many2one(
        'res.company', string='Company', index=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        related='company_id.currency_id', readonly=True)
