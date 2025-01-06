from odoo import models, api, fields


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    invoice_id = fields.Many2one('account.move', string='Invoice',
                                domain="[('state', '=', 'posted')]")