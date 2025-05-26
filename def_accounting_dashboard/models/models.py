from odoo import models, api, _, fields
from odoo.osv import expression


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        """Populate all bank and cash journal's data dict with relevant information for the kanban card."""
        bank_cash_journals = self.filtered(lambda journal: journal.type in ('bank', 'cash'))
        if not bank_cash_journals:
            return

        # Number to reconcile
        self._cr.execute("""
            SELECT st_line_move.journal_id,
                   COUNT(st_line.id)
              FROM account_bank_statement_line st_line
              JOIN account_move st_line_move ON st_line_move.id = st_line.move_id
             WHERE st_line_move.journal_id IN %s
               AND NOT st_line.is_reconciled
               AND st_line_move.to_check IS NOT TRUE
               AND st_line_move.state = 'posted'
               AND st_line_move.company_id IN %s
          GROUP BY st_line_move.journal_id
        """, [tuple(bank_cash_journals.ids), tuple(self.env.companies.ids)])
        number_to_reconcile = {
            journal_id: count
            for journal_id, count in self.env.cr.fetchall()
        }

        # Last statement
        bank_cash_journals.last_statement_id.mapped(lambda s: s.balance_end_real)  # prefetch

        outstanding_pay_account_balances = bank_cash_journals._get_journal_dashboard_outstanding_payments()

        # Payment with method outstanding account == journal default account
        direct_payment_balances = bank_cash_journals._get_direct_bank_payments()

        # Misc Entries (journal items in the default_account not linked to bank.statement.line)
        misc_domain = []
        for journal in bank_cash_journals:
            date_limit = journal.last_statement_id.date or journal.company_id.fiscalyear_lock_date
            misc_domain.append(
                [('account_id', '=', journal.default_account_id.id), ('date', '>', date_limit)]
                if date_limit else
                [('account_id', '=', journal.default_account_id.id)]
            )
        misc_domain = [
            *self.env['account.move.line']._check_company_domain(self.env.companies),
            ('statement_line_id', '=', False),
            ('parent_state', '=', 'posted'),
            ('payment_id', '=', False),
      ] + expression.OR(misc_domain)

        misc_totals = {
            account: (balance, count_lines, currencies)
            for account, balance, count_lines, currencies in self.env['account.move.line']._read_group(
                domain=misc_domain,
                aggregates=['amount_currency:sum', 'id:count', 'currency_id:recordset'],
                groupby=['account_id'])
        }

        # To check
        to_check = {
            journal: (amount, count)
            for journal, amount, count in self.env['account.bank.statement.line']._read_group(
                domain=[
                    ('journal_id', 'in', bank_cash_journals.ids),
                    ('move_id.company_id', 'in', self.env.companies.ids),
                    ('move_id.to_check', '=', True),
                    ('move_id.state', '=', 'posted'),
                ],
                groupby=['journal_id'],
                aggregates=['amount:sum', '__count'],
            )
        }

        for journal in bank_cash_journals:
            # User may have read access on the journal but not on the company
            currency = journal.currency_id or self.env['res.currency'].browse(journal.company_id.sudo().currency_id.id)
            has_outstanding, outstanding_pay_account_balance = outstanding_pay_account_balances[journal.id]
            to_check_balance, number_to_check = to_check.get(journal, (0, 0))
            misc_balance, number_misc, misc_currencies = misc_totals.get(journal.default_account_id, (0, 0, currency))
            currency_consistent = misc_currencies == currency
            accessible = journal.company_id.id in journal.company_id._accessible_branches().ids
            nb_direct_payments, direct_payments_balance = direct_payment_balances[journal.id]

            dashboard_data[journal.id].update({
                'number_to_check': number_to_check,
                'to_check_balance': currency.format(to_check_balance),
                'number_to_reconcile': number_to_reconcile.get(journal.id, 0),
                'account_balance': currency.format(journal.current_statement_balance),
                'has_at_least_one_statement': bool(journal.last_statement_id),
                'nb_lines_bank_account_balance': (bool(journal.has_statement_lines) or bool(nb_direct_payments)) and accessible,
                'outstanding_pay_account_balance': currency.format(outstanding_pay_account_balance),
                'nb_lines_outstanding_pay_account_balance': has_outstanding,
                'last_balance': currency.format(journal.last_statement_id.balance_end_real),
                'last_statement_id': journal.last_statement_id.id,
                'bank_statements_source': journal.bank_statements_source,
                'is_sample_data': journal.has_statement_lines,
                'nb_misc_operations': number_misc,
                'misc_class': 'text-warning' if not currency_consistent else '',
                'misc_operations_balance': currency.format(misc_balance) if currency_consistent else None,
            })

    def _get_journal_dashboard_bank_running_balance(self):
        # In order to not recompute everything from the start, we take the last
        # bank statement and only sum starting from there.
        self._cr.execute("""
            SELECT journal.id AS journal_id,
            COALESCE(SUM(aml.balance), 0.0)  AS balance_end_real,
            COALESCE(SUM(aml.amount_currency), 0.0) AS amount_currency,
            aml.currency_id AS currency_id,
            journal.currency_id AS journal_currency   
            from account_journal journal
            left join account_move_line aml on journal.default_account_id = aml.account_id and aml.parent_state = 'posted'
            where aml.company_id = ANY(%s) and journal.id = ANY(%s)
            group by journal.id, aml.currency_id, journal.currency_id
        """, [self.env.companies.ids, self.ids])
        query_res = {res['journal_id']: res for res in self.env.cr.dictfetchall()}
        result = {}
        for journal in self:
            journal_vals = query_res[journal.id] if journal.id in query_res.keys() else {"journal_id": journal.id, "balance_end_real": 0, "amount_currency": 0, "journal_currency": journal.currency_id.id}
            # print(journal_vals['balance_end_real'] if journal_vals[
            #                                             'journal_currency'] == self.env.company.currency_id.id else
            #     journal_vals['amount_currency'])
            result[journal.id] = (
                bool(journal_vals['journal_id']),
                journal_vals['balance_end_real'] if journal_vals[
                                                        'journal_currency'] == self.env.company.currency_id.id else
                journal_vals['amount_currency'],
            )
        return result


class BankRecWidgetLine(models.Model):
    _inherit = "bank.rec.widget.line"

    account_id = fields.Many2one(
        comodel_name='account.account',
        compute='_compute_account_id',
        store=True,
        readonly=False,
        check_company=True,
        domain=[['deprecated', '=', False], ['account_type', '!=', 'off_balance']],
    )