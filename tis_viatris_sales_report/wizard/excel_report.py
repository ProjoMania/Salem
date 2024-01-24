# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

from odoo import api, fields, models


class ExcelReport(models.TransientModel):
    _name = "excel.report"

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)
