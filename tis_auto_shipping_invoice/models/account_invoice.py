# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _validate_invoice(self):
        return self.sudo().action_post()
