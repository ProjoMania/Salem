from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def reconcile_payments(self, move_ids):
        _logger = logging.getLogger(__name__)
        _logger.info("Starting reconcile_payments...")
        moves = self.with_context(company_ids = [32, 2]).search([('id', 'in', move_ids)])
        
        total_moves = len(moves)
        _logger.info(f"Total moves to process: {total_moves}")
        
        error_move_ids = []  # List to track moves with errors
        error_details = {}  # Dict to track error messages for each move
        processed = 0
        
        move_ids = moves.ids
        batch_size = 250  # Process 10 invoices at a time
        _logger.info(f"Processing in batches of {batch_size}")
        
        for start_idx in range(0, len(move_ids), batch_size):
            batch = move_ids[start_idx:start_idx + batch_size]
            _logger.info(f"\nProcessing batch starting at index {start_idx}")
            batch_errors = []
            
            for move_id in batch:
                try:
                    _logger.info(f"Processing move ID: {move_id}")
                    move = self.with_context(company_ids = [32, 2]).env['account.move'].browse(move_id)
                    # Store lines to reassign later
                    pay_term_lines = move.line_ids.filtered(
                        lambda line: line.account_type in ('asset_receivable', 'liability_payable'))
                    invoice_partials = []
                    partial_list = []

                    for partial in pay_term_lines.matched_debit_ids:
                        partial_list.append(partial.id)
                        if partial.credit_move_id.id in move.line_ids.ids:
                            invoice_partials.append(partial.debit_move_id)
                        else:
                            invoice_partials.append(partial.credit_move_id)

                    for partial in pay_term_lines.matched_credit_ids:
                        partial_list.append(partial.id)
                        if partial.debit_move_id.id in move.line_ids.ids:
                            invoice_partials.append(partial.credit_move_id)
                        else:
                            invoice_partials.append(partial.debit_move_id)
                    
                    # Remove all outstanding partials
                    if partial_list:
                        _logger.info(f"Removing {len(partial_list)} outstanding partials")
                        move.with_context(company_ids = [32, 2]).call_js_remove_outstanding_partials(partial_list)
                        pay_term_lines._compute_amount_residual()
                        # Re-assign lines
                        _logger.info(f"Re-assigning {len(invoice_partials)} lines")
                        for line in invoice_partials:
                            move.with_context(company_ids = [32, 2]).call_js_assign_outstanding_line(line.id)
                        
                    self.env.cr.commit()
                    _logger.info(f"Successfully processed move ID: {move_id}")

                except Exception as e:
                    self.env.cr.rollback()
                    if move_id not in error_move_ids and move_id not in batch_errors:
                        batch_errors.append(move_id)
                        error_details[move_id] = str(e)
                        _logger.error(f"Error processing move ID {move_id}: {e}")
                
                processed += 1
                progress = int(50 * processed / total_moves)
                _logger.info(f"Progress: {processed}/{total_moves} moves ({(processed/total_moves*100):.1f}%)")
                
            self.env.cr.execute("select setval('mail_tracking_value_id_seq', (select max(id) from mail_tracking_value));")
            self.env.cr.commit()
            error_move_ids.extend([x for x in batch_errors if x not in error_move_ids])
            _logger.info(f"Completed batch. Errors in this batch: {len(batch_errors)}")
        
        _logger.info("\n=== RECONCILIATION REPORT ===")
        _logger.info(f"Total moves processed: {total_moves}")
        _logger.info(f"Successful moves: {total_moves - len(error_move_ids)}")
        _logger.info(f"Failed moves: {len(error_move_ids)}")
        if error_move_ids:
            _logger.info("\nDetailed Error Report:")
            for move_id in error_move_ids:
                _logger.info(f"Move ID {move_id}: {error_details.get(move_id, 'Unknown error')}")
        _logger.info("===========================")
        
        return True


    def reset_exchange_entries(self, company_id, journal_id):
        moves = self.search([('journal_id', '=', journal_id), ('company_id', '=', company_id), ('state', '=', 'posted')])
        processed_moves = set()
        processed_moves.add(495812)

        for move in moves:
            full_reconcile_id = self.env['account.partial.reconcile'].search([('exchange_move_id', '=', move.id)])
            if full_reconcile_id:
                full_reconcile_id.write({'exchange_move_id': False})
            if move.id in processed_moves:
                continue
            matched_debits = move.mapped('line_ids').mapped('matched_debit_ids')
            matched_credits = move.mapped('line_ids').mapped('matched_credit_ids')
            
            if not matched_debits and not matched_credits:
                try:
                    move.call_draft()
                    move.call_cancel()
                    processed_moves.add(move.id)
                except Exception as e:
                    return e
                continue
            # elif any(line.currency_id.id == 87 for line in move.line_ids.mapped('matched_debit_ids.credit_move_id')) or \
            #      any(line.currency_id.id == 87 for line in move.line_ids.mapped('matched_credit_ids.debit_move_id')):
            #     print(f"Move {move.id} is reconciled with invoice in currency ID 87")
            #     try:
            #         # Get the invoice IDs with currency 87
            #         invoice_ids = []
            #         for line in move.line_ids:
            #             invoice_ids.extend([ml.move_id.id for ml in line.matched_debit_ids.mapped('credit_move_id')
            #                                if ml.currency_id.id == 87 and ml.move_id.move_type == 'out_invoice'])
            #             invoice_ids.extend([ml.move_id.id for ml in line.matched_credit_ids.mapped('debit_move_id')
            #                                if ml.currency_id.id == 87 and ml.move_id.move_type == 'out_invoice'])
            #
            #         if invoice_ids:
            #             print(f"Found invoices with currency 87: {invoice_ids}")
            #             # Pass the invoice IDs to bulk_reassign_reconcile method
            #             self.bulk_reassign_reconcile(invoice_ids)
            #             processed_moves.add(move.id)
            #             print(f"Successfully processed move {move.id} with bulk_reassign_reconcile")
            #     except Exception as e:
            #         print(f"Error processing move {move.id} with currency 87: {e}")
            #     continue
            
            # Find all reconciled moves
            all_reconciled_moves = set()
            same_journal_moves = set()
            
            for debit in matched_debits:
                all_reconciled_moves.add(debit.credit_move_id.move_id.id)
                all_reconciled_moves.add(debit.debit_move_id.move_id.id)
                if debit.credit_move_id.move_id.journal_id.id == journal_id:
                    same_journal_moves.add(debit.credit_move_id.move_id.id)
                if debit.debit_move_id.move_id.journal_id.id == journal_id:
                    same_journal_moves.add(debit.debit_move_id.move_id.id)
                    
            for credit in matched_credits:
                all_reconciled_moves.add(credit.credit_move_id.move_id.id)
                all_reconciled_moves.add(credit.debit_move_id.move_id.id)
                if credit.credit_move_id.move_id.journal_id.id == journal_id:
                    same_journal_moves.add(credit.credit_move_id.move_id.id)
                if credit.debit_move_id.move_id.journal_id.id == journal_id:
                    same_journal_moves.add(credit.debit_move_id.move_id.id)
            
            
            # Check if there are any reconciled moves from different journals
            other_journal_moves = all_reconciled_moves - same_journal_moves
            if other_journal_moves:
                continue
                
            # Reset both the current move and its reconciled moves from the same journal
            if same_journal_moves:
                same_journal_moves.add(move.id)
                for move_id in same_journal_moves:
                    if move_id in processed_moves:
                        continue
                    try:
                        self.browse(move_id).call_draft()
                        self.browse(move_id).call_cancel()
                        processed_moves.add(move_id)
                    except Exception as e:
                        return e
        
        return True

    def call_draft(self):
        self.button_draft()
        return True

    def call_cancel(self):
        self.button_cancel()
        return True

    def comp_amount(self, comp_id):
        records = self.search([('company_id', '=', comp_id), ('state', '=', 'posted'), ('move_type', '!=', 'entry')])
        for rec in records:
            rec._compute_amount()
        return True

    def bulk_reassign_reconcile(self, move_ids):
        """
        Remove multiple outstanding payment lines at once.

        Args:
            line_ids (list): List of partial payment line IDs to remove

        Returns:
            bool: True on success
        """
        self = self.with_context(company_ids=[2, 32])
        
        # Pre-browse all moves to avoid repeated database calls
        moves_dict = {move.id: move for move in self.browse(move_ids)}
        
        # Process out_invoice moves first
        invoice_moves = []
        other_moves = []
        for move_id in move_ids:
            move = moves_dict[move_id]
            if move.move_type == 'out_invoice':
                invoice_moves.append(move)
            else:
                other_moves.append(move)
        
        
        
        # Process invoice moves
        invoice_move_data = []
        for i, move in enumerate(invoice_moves):
            pay_term_lines = move.line_ids.filtered(lambda line: line.account_type in ('asset_receivable', 'liability_payable'))
            invoice_partials = []
            partial_list = []
            
            # Collect all partials in one pass
            for partial in pay_term_lines.matched_debit_ids:
                partial_list.append(partial.id)
                if partial.credit_move_id.id in move.line_ids.ids:
                    invoice_partials.append(partial.debit_move_id)
                else:
                    invoice_partials.append(partial.credit_move_id)
                    
            for partial in pay_term_lines.matched_credit_ids:
                partial_list.append(partial.id)
                if partial.debit_move_id.id in move.line_ids.ids:
                    invoice_partials.append(partial.credit_move_id)
                else:
                    invoice_partials.append(partial.debit_move_id)
            
            invoice_move_data.append((move, partial_list, invoice_partials))
            
            # Remove all partials first
            for j, par in enumerate(partial_list):
                try:
                    move.js_remove_outstanding_partial(par)
                except Exception as e:
                    return e
        
        # Process other moves
        other_move_data = []
        for i, move in enumerate(other_moves):
            pay_term_lines = move.line_ids.filtered(lambda line: line.account_type in ('asset_receivable', 'liability_payable'))
            invoice_partials = {}
            partial_list = []
            
            # Process matched_debit_ids
            for partial in pay_term_lines.matched_debit_ids:
                partial_list.append(partial.id)
                if partial.credit_move_id.id in move.line_ids.ids:
                    debit_move = partial.debit_move_id
                    if debit_move.move_id.move_type == 'out_invoice':
                        invoice_partials.setdefault(debit_move.move_id, []).append(partial.credit_move_id)
                else:
                    credit_move = partial.credit_move_id
                    if credit_move.move_id.move_type == 'out_invoice':
                        invoice_partials.setdefault(credit_move.move_id, []).append(partial.debit_move_id)
            
            # Process matched_credit_ids
            for partial in pay_term_lines.matched_credit_ids:
                partial_list.append(partial.id)
                if partial.debit_move_id.id in move.line_ids.ids:
                    credit_move = partial.credit_move_id
                    if credit_move.move_id.move_type == 'out_invoice':
                        invoice_partials.setdefault(credit_move.move_id, []).append(partial.debit_move_id)
                else:
                    debit_move = partial.debit_move_id
                    if debit_move.move_id.move_type == 'out_invoice':
                        invoice_partials.setdefault(debit_move.move_id, []).append(partial.credit_move_id)
            
            other_move_data.append((move, partial_list, invoice_partials))
            
            # Remove all partials first
            for j, par in enumerate(partial_list):
                try:
                    move.js_remove_outstanding_partial(par)
                except Exception as e:
                    return e
        
        # Execute SQL update after all removals
        self.env.cr.execute("update account_move_line set amount_residual = amount_residual_currency where currency_id = company_currency_id and company_id = 32;")
        self.env.cr.commit()
        
        # Now reassign all partials for invoice moves
        for i, (move, _, invoice_partials) in enumerate(invoice_move_data):
            for j, line in enumerate(invoice_partials):
                try:
                    move.js_assign_outstanding_line(line.id)
                except Exception as e:
                    return e
        
        # Now reassign all partials for other moves
        for i, (move, _, invoice_partials_dict) in enumerate(other_move_data):
            for mov, lines in invoice_partials_dict.items():
                for j, line in enumerate(lines):
                    try:
                        mov.js_assign_outstanding_line(line.id)
                        mov.js_assign_outstanding_line(line.id)
                    except Exception as e:
                        return e
        
        return True

    def call_js_remove_outstanding_partials(self, x_list):
        for x in x_list:
            try:
                self.js_remove_outstanding_partial(x)
            except:
                return x

    # def call_js_assign_outstanding_lines(self, x_list):
    #     print(self)
    #     for x in x_list:
    #         try:
    #             self.call_js_assign_outstanding_line(x)
    #         except:
    #             print("Error")
    #     return True

    def call_js_assign_outstanding_line(self, x):
        # if self.payment_state != 'paid':
        self.js_assign_outstanding_line(x)
        return True


class Product(models.Model):
    _inherit = 'product.product'

    def call_run_fifo_vacuum(self, company):
        prods = self.search([('company_id', '=', company)])
        for prod in prods:
            prod._run_fifo_vacuum()
        prods._compute_quantities()

        # Refresh the valuation layers
        prods._compute_value_svl()
        valuation_layers = self.env['stock.valuation.layer'].search([
            ('product_id', 'in', prods.ids),
            ('company_id', '=', company)
        ])
        if valuation_layers:
            valuation_layers.remaining_qty
            valuation_layers.remaining_value

        # Invalidate cache to ensure fresh computations
        prods.invalidate_cache()
        return True

class Accountmoveline(models.Model):
    _inherit = "account.move.line"

    x_studio_field_uRnfp = fields.Selection(name="New Related Field", selection=[])


class Accountpayment(models.Model):
    _inherit = "account.payment"

    x_studio_field_Gb6C2 = fields.Many2one(name="Employee", comodel_name="hr.employee")
    x_studio_payment_type_ = fields.Char(name="طريقة السداد", )


class Hrapplicant(models.Model):
    _inherit = "hr.applicant"

    x_studio_field_9uX2K = fields.Selection(name="New Priority", selection=[('Very High', '3'), ('High', '2'),
                                                                            ('Low', '1'), ('Normal', '0')])
    x_studio_age = fields.Float(name="Age", )
    x_studio_years_or_experience = fields.Float(name="Years or Experience ", )
    x_studio_city = fields.Many2one(name="City", comodel_name="res.country.state")
    x_studio_photo = fields.Binary(name="Photo", )
    x_studio_field_lEDEP = fields.Float(name="New Decimal", )
    x_studio_field_of_study_1 = fields.Char(name="Field of Study", )


class Hrcontract(models.Model):
    _inherit = "hr.contract"

    x_studio_field_TqTNl = fields.Char(name="New Related Field", )


# class Hremployee(models.Model):
#     _inherit = "hr.employee"

   # x_studio_work_permit_expire = fields.Date(name="Work Permit Expire", )
   # x_studio_passport_expire = fields.Date(name="Passport Expire", )
    #x_studio_recidency_expire = fields.Date(name="Recidency Expire", )


class Hrpayslip(models.Model):
    _inherit = "hr.payslip"

    x_studio_city = fields.Char(name="City", )


class Purchaseorder(models.Model):
    _inherit = "purchase.order"

    x_studio_payment_type_ = fields.Char(name="Payment Type :", )
    x_studio_shipping_to_ = fields.Char(name="Shipping to :", )
    
    def ccompute_invoice(self, comp_id):
        records = self.search([("company_id", '=', comp_id)])
        for rec in records:
            rec._compute_invoice()
        return True

    def ccompute_picking_ids(self, comp_id):
        records = self.search([("company_id", '=', comp_id)])
        for rec in records:
            rec._compute_picking_ids()
        return True


class Rescompany(models.Model):
    _inherit = "res.company"

    x_studio_background_report = fields.Binary(name="Background Report", )


class Stockmoveline(models.Model):
    _inherit = "stock.move.line"

    x_studio_demand = fields.Float(name="Demand", )
