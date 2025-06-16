
from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    receive_daily_SO_reports = fields.Boolean(string='Receive SO Report Daily')