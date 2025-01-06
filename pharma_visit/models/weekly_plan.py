
from odoo import models, fields


class WeeklyPlan(models.Model):
    _name = "weekly.plan"
    _rec_name = 'partner_id'
    _description = "Weekly Plan"

    partner_id = fields.Many2one('res.partner', string="Doctor's Name", required=True)
    date = fields.Date(string="Date")
    area = fields.Char(string="Area")
    description = fields.Text(string="Description")
