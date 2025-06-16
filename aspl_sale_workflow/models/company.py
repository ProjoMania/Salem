
from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    enable_multiple_workflows = fields.Boolean(string='Enable Multiple Workflows')