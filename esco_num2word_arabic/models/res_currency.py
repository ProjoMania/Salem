# -*- coding: utf-8 -*-

import logging
import math
import re
import time
import traceback

from odoo import api, fields, models, tools, _
from odoo.tools.misc import get_lang

_logger = logging.getLogger(__name__)


class Currency(models.Model):
    _inherit = "res.currency"

    name = fields.Char(string='Currency', size=3, required=True, help="Currency Code (ISO 4217)")
    currency_unit_label = fields.Char(string="Currency Unit", help="Currency Unit Name", translate=False)
    currency_subunit_label = fields.Char(string="Currency Subunit", help="Currency Subunit Name", translate=False)
