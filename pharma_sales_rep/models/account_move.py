
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    sales_rep_id = fields.Many2one('res.users', string='Sales Representative', domain=lambda self: [
        ("groups_id", "=", self.env.ref("pharma_sales_rep.group_sales_rep").id)], default=lambda self: self.env.user)
