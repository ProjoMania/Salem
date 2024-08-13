from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

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
            result[journal.id] = (
                bool(journal_vals['journal_id']),
                journal_vals['balance_end_real'] if journal_vals[
                                                        'journal_currency'] == self.env.company.currency_id.id else
                journal_vals['amount_currency'],
            )
        return result