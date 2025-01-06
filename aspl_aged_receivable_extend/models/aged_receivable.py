# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import formatLang, format_date


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner.balance.report.handler"

    def set_currency_option(self):
        currency_id = self.env.context.get('currency_id')
        self._get_sql()
        return currency_id

    def get_updated_rate(self, currency_id):
        currency_rate = self.env['res.currency'].browse(currency_id)
        final_rate = currency_rate.rate_ids[0].company_rate if currency_rate.rate_ids else currency_rate.rate
        return final_rate

    def _get_sql(self):
        if self.env.context.get('is_extend') or self.env.context.get('report_options') and self.env.context.get(
                'report_options').get('currency_id'):

            options = self.env.context['report_options']
            currency_rate = self.get_updated_rate(int(options.get('currency_id')))

            query = ("""
                SELECT
                    account_move_line.id, account_move_line.move_id, account_move_line.name, account_move_line.account_id, account_move_line.journal_id, account_move_line.company_id, {option_currency_id} AS currency_id, account_move_line.analytic_account_id, account_move_line.display_type, account_move_line.date, account_move_line.debit, account_move_line.credit, account_move_line.balance,
                    account_move_line.partner_id AS partner_id,
                    account_move_line.amount_currency * {currency_rate} as amount_currency ,
                    partner.name AS partner_name,
                    COALESCE(trust_property.value_text, 'normal') AS partner_trust,
                    COALESCE({option_currency_id}, journal.currency_id) AS report_currency_id,
                    account_move_line.payment_id AS payment_id,
                    COALESCE(account_move_line.date_maturity, account_move_line.date) AS report_date,
                    account_move_line.expected_pay_date AS expected_pay_date,
                    move.move_type AS move_type,
                    move.name AS move_name,
                    move.ref AS move_ref,
                    account.code || ' ' || account.name AS account_name,
                    account.code AS account_code,""" + ','.join([("""
                    CASE WHEN period_table.period_index = {i}
                    THEN %(sign)s * ROUND((
                        account_move_line.balance - COALESCE(SUM(part_debit.amount), 0) + COALESCE(SUM(part_credit.amount), 0)
                    ) * currency_table.rate, currency_table.precision)
                    ELSE 0 END AS period{i}""").format(i=i) for i in range(6)]) + """
                FROM account_move_line
                JOIN account_move move ON account_move_line.move_id = move.id
                JOIN account_journal journal ON journal.id = account_move_line.journal_id
                JOIN account_account account ON account.id = account_move_line.account_id
                LEFT JOIN res_partner partner ON partner.id = account_move_line.partner_id
                LEFT JOIN ir_property trust_property ON (
                    trust_property.res_id = 'res.partner,'|| account_move_line.partner_id
                    AND trust_property.name = 'trust'
                    AND trust_property.company_id = account_move_line.company_id
                )
                JOIN {currency_table} ON currency_table.company_id = account_move_line.company_id
                LEFT JOIN LATERAL (
                    SELECT part.amount, part.debit_move_id
                    FROM account_partial_reconcile part
                    WHERE part.max_date <= %(date)s
                ) part_debit ON part_debit.debit_move_id = account_move_line.id
                LEFT JOIN LATERAL (
                    SELECT part.amount, part.credit_move_id
                    FROM account_partial_reconcile part
                    WHERE part.max_date <= %(date)s
                ) part_credit ON part_credit.credit_move_id = account_move_line.id
                JOIN {period_table} ON (
                    period_table.date_start IS NULL
                    OR COALESCE(account_move_line.date_maturity, account_move_line.date) <= DATE(period_table.date_start)
                )
                AND (
                    period_table.date_stop IS NULL
                    OR COALESCE(account_move_line.date_maturity, account_move_line.date) >= DATE(period_table.date_stop)
                )
                WHERE account.internal_type = %(account_type)s
                AND account.exclude_from_aged_reports IS NOT TRUE
                GROUP BY account_move_line.id, partner.id, trust_property.id, journal.id, move.id, account.id,
                        period_table.period_index, currency_table.rate, currency_table.precision
                HAVING ROUND(account_move_line.balance - COALESCE(SUM(part_debit.amount), 0) + COALESCE(SUM(part_credit.amount), 0), currency_table.precision) != 0
            """).format(
                move_line_fields=self._get_move_line_fields('account_move_line'),
                currency_table=self.env['res.currency']._get_query_currency_table(options),
                period_table=self._get_query_period_table(options),
                option_currency_id=int(options.get('currency_id')),
                currency_rate=currency_rate
            )
            params = {
                'account_type': options['filter_account_type'],
                'sign': 1 if options['filter_account_type'] == 'receivable' else -1,
                'date': options['date']['date_to'],
            }

            return self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)

        else:
            return super(ReportAccountAgedPartner, self)._get_sql()


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    filter_currency = True

    def set_currency_id(self):
        if self.env.context and self.env.context.get('is_extend') or self.env.context.get('report_options').get(
                'currency_id'):
            currency_id = int(self.env.context.get('report_options').get('currency_id'))
        else:
            currency_id = self.env.company.currency_id.id
        return currency_id

    def format_value(self, amount, currency=False, blank_if_zero=False):
        if self.env.context.get('is_extend') or (
                self.env.context.get('report_options') and self.env.context.get('report_options').get('currency_id')):
            currency_id = self.env['res.currency'].browse(self.set_currency_id())
            if currency_id.is_zero(amount):
                if blank_if_zero:
                    return ''
                amount = abs(amount)

            if self.env.context.get('no_format'):
                return amount
            return formatLang(self.env, amount, currency_obj=currency_id)
        else:
            return super().format_value(amount, currency=currency, blank_if_zero=blank_if_zero)

    @api.model
    def _init_filter_currency(self, options, previous_options=None):
        if not self.filter_currency:
            return

        if self.env.context.get('is_extend'):
            options['currency'] = True
            options['currency_id'] = previous_options and previous_options.get(
                'currency_id') or self.env.company.currency_id.id


class ResCurrencyData(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_query_currency_table(self, options):
        ''' Construct the currency table as a mapping company -> rate to convert the amount to the user's company
        currency in a multi-company/multi-currency environment.
        The currency_table is a small postgresql table construct with VALUES.
        :param options: The report options.
        :return:        The query representing the currency table.
        '''
        if self.env.context.get('is_extend') or (
                self.env.context.get('report_options') and self.env.context.get('report_options').get('currency_id')):

            user_company = self.env.company
            user_currency = user_company.currency_id
            if options.get('multi_company', False):

                companies = self.env.companies
                conversion_date = options['date']['date_to']
                currency_rates = companies.mapped('currency_id')._get_rates(user_company, conversion_date)
            else:
                companies = user_company
                currency_rates = {user_currency.id: 1.0}

            conversion_rates = []
            user_currency = self.env['res.currency'].browse(int(options.get('currency_id')))
            for company in companies:
                conversion_rates.extend((
                    company.id,

                    int(options.get('currency_id')) if options.get('currency_id') else self.env.company.currency_id.id,

                    # ? Base code
                    # currency_rates[user_company.currency_id.id] / currency_rates[company.currency_id.id],
                    user_currency.decimal_places,
                ))
            # query = '(VALUES %s) AS currency_table(company_id, rate, precision)' % ','.join(
            #     '(%s, %s, %s)' for i in companies)
            query = f'(VALUES ({self.env.company.id},{user_currency.rate},{user_currency.decimal_places}) ) AS currency_table(company_id, rate, precision)'
            return self.env.cr.mogrify(query, conversion_rates).decode(self.env.cr.connection.encoding)
        else:
            return super(ResCurrencyData, self)._get_query_currency_table(options)


class ReportAccountAgedReceivableNew(models.Model):
    _name = "account.aged.receivable.extend"
    _description = "Aged Receivable Extend"
    _inherit = "account.aged.partner.balance.report.handler"
    _auto = False



    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(ReportAccountAgedReceivableNew, self)._get_options(previous_options=previous_options)
        options['filter_account_type'] = 'receivable'
        return options

    @api.model
    def _get_report_name(self):
        return _("Aged Receivable")

    @api.model
    def _get_templates(self):
        # OVERRIDE
        templates = super(ReportAccountAgedReceivableNew, self)._get_templates()
        templates['line_template'] = 'aspl_aged_receivable_extend.line_template_aged_receivable_report_new'
        return templates
