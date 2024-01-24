# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = "res.users"

    signature_image = fields.Binary(string="Signature Image", attachment=True)
