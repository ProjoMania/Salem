# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

from odoo import api, fields, models
from datetime import date


class ResPartner(models.Model):
    _inherit = "res.partner"

    cash_collection_team_id = fields.Many2one('cash.collection.teams', string='Cash Collection Team')
