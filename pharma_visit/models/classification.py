
from odoo import models, fields, _


class Classification(models.Model):
    _name = "doctor.classification"
    _rec_name = 'name'
    _description = "Classification"

    name = fields.Char(string="Name")
