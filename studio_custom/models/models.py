from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def reset_exchange_entries(self, company_id, journal_id):
        moves = self.search([('journal_id', '=', journal_id), ('company_id', '=', company_id)])
        for move in moves:
            print(move.name)
            if move.mapped('line_ids').mapped('matched_debit_ids') or move.mapped('line_ids').mapped('matched_credit_ids'):
                continue
            try:
                move.call_draft()
                move.call_cancel()
            except Exception as e:
                print(e)
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
            print(rec.line_ids.mapped('account_id'))
            print(rec.name)
            rec._compute_amount()
            print(rec.amount_untaxed_signed)
        return True

    def bulk_reassign_reconcile(self, move_ids):
        """
        Remove multiple outstanding payment lines at once.

        Args:
            line_ids (list): List of partial payment line IDs to remove

        Returns:
            bool: True on success
        """
        self = self.with_context(company_ids = [2, 32])
        print(move_ids)
        print(len(move_ids))
        other_move_ids = []
        for move_id in move_ids:
            move = self.browse(move_id)
            if move.currency_id.id != 87:
                continue
            if move.move_type != 'out_invoice':
                other_move_ids.append(move_id)
                continue
            pay_term_lines = move.line_ids \
                .filtered(lambda line: line.account_type in ('asset_receivable', 'liability_payable'))
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
            print(move.name)
            for par in partial_list:
                try:
                    move.js_remove_outstanding_partial(par)
                except:
                    print("ERROR REMOVE")
                    continue
            self.env.cr.execute("update account_move_line set amount_residual = amount_residual_currency where currency_id = company_currency_id and company_id = 32;")
            self.env.cr.commit()
            for line in invoice_partials:
                print("line")
                print(line)
                try:
                    print(move, line)
                    move.js_assign_outstanding_line(line.id)
                except:
                    print("Error Assign")
                    continue
        for move_id in other_move_ids:
            move = self.browse(move_id)
            pay_term_lines = move.line_ids \
                .filtered(lambda line: line.account_type in ('asset_receivable', 'liability_payable'))
            invoice_partials = {}
            partial_list = []
            for partial in pay_term_lines.matched_debit_ids:
                partial_list.append(partial.id)
                if partial.credit_move_id.id in move.line_ids.ids:
                    if partial.debit_move_id.move_id.move_type == 'out_invoice':
                        if partial.debit_move_id.move_id in invoice_partials.keys():
                            invoice_partials[partial.debit_move_id.move_id].append(partial.credit_move_id)
                        else:
                            invoice_partials.update({partial.debit_move_id.move_id: [partial.credit_move_id]})
                else:
                    if partial.credit_move_id.move_id.move_type == 'out_invoice':
                        if partial.credit_move_id.move_id in invoice_partials.keys():
                            invoice_partials[partial.credit_move_id.move_id].append(partial.debit_move_id)
                        else:
                            invoice_partials.update({partial.credit_move_id.move_id: [partial.debit_move_id]})
            for partial in pay_term_lines.matched_credit_ids:
                partial_list.append(partial.id)
                if partial.debit_move_id.id in move.line_ids.ids:
                    if partial.credit_move_id.move_id.move_type == 'out_invoice':
                        if partial.credit_move_id.move_id in invoice_partials.keys():
                            invoice_partials[partial.credit_move_id.move_id].append(partial.debit_move_id)
                        else:
                            invoice_partials.update(
                                {partial.credit_move_id.move_id: [partial.debit_move_id]})
                else:
                    if partial.debit_move_id.move_id.move_type == 'out_invoice':
                        if partial.debit_move_id.move_id in invoice_partials.keys():
                            invoice_partials[partial.debit_move_id.move_id].append(partial.credit_move_id)
                        else:
                            invoice_partials.update({partial.debit_move_id.move_id: [partial.credit_move_id]})
            print(move.name)
            for par in partial_list:
                try:
                    move.js_remove_outstanding_partial(par)
                except:
                    print("ERROR REMOVE")
                    continue
            self.env.cr.execute("update account_move_line set amount_residual = amount_residual_currency where currency_id = company_currency_id and company_id = 32;")
            self.env.cr.commit()
            for mov in invoice_partials.keys():
                print(mov)
                for line in invoice_partials[mov]:
                    try:
                        print(mov, line)
                        mov.js_assign_outstanding_line(line.id)
                    except:
                        print("Error Assign")
                        continue
        return True

    def call_js_remove_outstanding_partials(self, x_list):
        print(x_list)
        for x in x_list:
            try:
                self.js_remove_outstanding_partial(x)
            except:
                print(x)
        return True

    # def call_js_assign_outstanding_lines(self, x_list):
    #     print(self)
    #     for x in x_list:
    #         try:
    #             self.call_js_assign_outstanding_line(x)
    #         except:
    #             print("Error")
    #     return True

    def call_js_assign_outstanding_line(self, x):
        print("self", self)
        # if self.payment_state != 'paid':
        self.js_assign_outstanding_line(x)
        return True


class Product(models.Model):
    _inherit = 'product.product'

    def call_run_fifo_vacuum(self, company):
        prods = self.search([('company_id', '=', company)])
        for prod in prods:
            print(company, prod.name)
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
            print(rec.picking_ids)
        return True

    def ccompute_picking_ids(self, comp_id):
        records = self.search([("company_id", '=', comp_id)])
        for rec in records:
            rec._compute_picking_ids()
            print(rec.picking_ids)
        return True


class Rescompany(models.Model):
    _inherit = "res.company"

    x_studio_background_report = fields.Binary(name="Background Report", )


class Stockmoveline(models.Model):
    _inherit = "stock.move.line"

    x_studio_demand = fields.Float(name="Demand", )
