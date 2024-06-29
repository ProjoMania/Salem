
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    # max_disc = fields.Float(string="Maximum Discount")
    disc_type = fields.Selection([('fix_amount', 'Fix Amount'), ('percentage', 'Percentage')],
                                     string="Discount Type", copy=False)
    max_disc_amt = fields.Monetary(string='Maximum Amount', required=False, tracking=True)
    max_disc_pt = fields.Float(string='Maximum Discount(%)', required=False, tracking=True)

