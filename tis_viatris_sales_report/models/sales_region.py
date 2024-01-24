# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

from odoo import api, models, _
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from datetime import datetime


class SalesRegion(models.Model):
    _name = 'sales.region'
    _description = 'sales region'

    name = fields.Char(string="Region", required=True)


