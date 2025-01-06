from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_id = fields.Char("Customer ID")
    

class AccountMove(models.Model):
    _inherit = 'account.move'
    

