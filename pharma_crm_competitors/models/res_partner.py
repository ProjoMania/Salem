# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    classification_id = fields.Many2one(comodel_name="customer.classification", string="Classification", domain="[('contact_id', '=', customer_type)]")
    