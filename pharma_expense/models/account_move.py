from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    expense_count = fields.Integer(string="# of Expenses", compute='_compute_expense_count')

    def _compute_expense_count(self):
        for move in self:
            expense_count = self.env['hr.expense'].search_count([('invoice_id', '=', move.id)])
            move.expense_count = expense_count
            
    def show_hr_expense(self):
        action = {
            'name':'HR Expense',
            'res_model':'hr.expense',
            'domain':[('invoice_id','=',self.id)],
            'context': {'default_invoice_id': self.id},
            'view_mode':'tree,form',
            'type': 'ir.actions.act_window',
            }
        return action
    

    