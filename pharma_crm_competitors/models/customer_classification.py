# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomerClassification(models.Model):
    _name = 'customer.classification'
    _description = 'Customer Classification'

    name = fields.Char(string="Name", required=True)
    contact_id = fields.Many2one(comodel_name='customer.type',string="Contact Type", required=True)