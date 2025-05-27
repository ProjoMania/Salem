# -*- coding: utf-8 -*-

from odoo import models, api, _


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id):
        """
        Override to fix the issue with NULL account_id values in account.move.lines
        Adds safety checks to ensure no NULL account_id values are ever created.
        """
        # Safety check to ensure we have valid account IDs
        if not debit_account_id:
            cost_product = self.cost_line_id.product_id
            accounts = cost_product.product_tmpl_id.get_product_accounts()
            debit_account_id = accounts.get('stock_valuation') and accounts['stock_valuation'].id or False
            if not debit_account_id and accounts.get('expense'):
                debit_account_id = accounts['expense'].id
            
        if not credit_account_id and debit_account_id:
            credit_account_id = debit_account_id
            
        if not already_out_account_id and debit_account_id:
            already_out_account_id = debit_account_id

        # Call the original method with safety-checked account IDs
        result = super(AdjustmentLines, self)._create_account_move_line(
            move, credit_account_id, debit_account_id, qty_out, already_out_account_id
        )
        
        # Additional safety check: ensure no line has a NULL account_id
        for line in result:
            if not line[2].get('account_id'):
                # Log this issue and fix it
                line[2]['account_id'] = debit_account_id or credit_account_id or self.cost_line_id.account_id.id
                
        return result
