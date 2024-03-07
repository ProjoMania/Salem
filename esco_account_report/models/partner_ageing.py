# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime
from itertools import chain
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import format_date


class report_account_aged_partner(models.AbstractModel):
    _name = "account.aged.partner.balance.report.handler"
    _inherit = "account.aged.partner.balance.report.handler"

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    period5 = fields.Monetary(string='121 - 150')
    period6 = fields.Monetary(string='151 - 180')
    period7 = fields.Monetary(string='Older')

    @api.model
    def _get_query_period_table(self, options):
        ''' Compute the periods to handle in the report.
        E.g. Suppose date = '2019-01-09', the computed periods will be:

        Name                | Start         | Stop
        --------------------------------------------
        As of 2019-01-09    | 2019-01-09    |
        1 - 30              | 2018-12-10    | 2019-01-08
        31 - 60             | 2018-11-10    | 2018-12-09
        61 - 90             | 2018-10-11    | 2018-11-09
        91 - 120            | 2018-09-11    | 2018-10-10
        Older               |               | 2018-09-10

        Then, return the values as an sql floating table to use it directly in queries.

        :return: A floating sql query representing the report's periods.
        '''
        def minus_days(date_obj, days):
            return fields.Date.to_string(date_obj - relativedelta(days=days))

        date_str = options['date']['date_to']
        date = fields.Date.from_string(date_str)
        period_values = [
            (False, date_str),
            (minus_days(date, 1), minus_days(date, 30)),
            (minus_days(date, 31), minus_days(date, 60)),
            (minus_days(date, 61), minus_days(date, 90)),
            (minus_days(date, 91), minus_days(date, 120)),
            (minus_days(date, 121), minus_days(date, 150)),
            (minus_days(date, 151), minus_days(date, 180)),
            (minus_days(date, 181), False),
        ]
        period_table = ('(VALUES %s) AS period_table(date_start, date_stop, period_index)' %
                        ','.join("(%s, %s, %s)" for i, period in enumerate(period_values)))
        params = list(chain.from_iterable(
            (period[0] or None, period[1] or None, i)
            for i, period in enumerate(period_values)
        ))
        return self.env.cr.mogrify(period_table, params).decode(self.env.cr.connection.encoding)

    @api.model
    def _get_sql(self):
        options = self.env.context['report_options']
        query = ("""
            SELECT
                {move_line_fields},
                account_move_line.amount_currency as amount_currency,
                account_move_line.partner_id AS partner_id,
                partner.name AS partner_name,
                COALESCE(trust_property.value_text, 'normal') AS partner_trust,
                COALESCE(account_move_line.currency_id, journal.currency_id) AS report_currency_id,
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
                ELSE 0 END AS period{i}""").format(i=i) for i in range(8)]) + """
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
        )
        params = {
            'account_type': options['filter_account_type'],
            'sign': 1 if options['filter_account_type'] == 'receivable' else -1,
            'date': options['date']['date_to'],
        }
        return self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)

    @api.model
    def _get_column_details(self, options):
        columns = [
            self._header_column(),
            self._field_column('report_date'),

            self._field_column('account_name', name=_("Account"), ellipsis=True),
            self._field_column('expected_pay_date'),
            self._field_column('period0', name=_("As of: %s", format_date(self.env, options['date']['date_to']))),
            self._field_column('period1', sortable=True),
            self._field_column('period2', sortable=True),
            self._field_column('period3', sortable=True),
            self._field_column('period4', sortable=True),
            self._field_column('period5', sortable=True),
            self._field_column('period6', sortable=True),
            self._field_column('period7', sortable=True),
            self._custom_column(  # Avoid doing twice the sub-select in the view
                name=_('Total'),
                classes=['number'],
                formatter=self.format_value,
                getter=(
                    lambda v: v['period0'] + v['period1'] + v['period2'] + v['period3'] + v['period4'] + v['period5'] + v['period6'] + v['period7']),
                sortable=True,
            ),
        ]

        if self.user_has_groups('base.group_multi_currency'):
            columns[2:2] = [
                self._field_column('amount_currency'),
                self._field_column('currency_id'),
            ]
        # for col in columns:
        #     print(col)
        # print('/////////////////////////////////////')
        return columns

    def _get_hierarchy_details(self, options):
        return [
            self._hierarchy_level('partner_id', foldable=True, namespan=len(self._get_column_details(options)) - 9),
            self._hierarchy_level('id'),
        ]

    def _show_line(self, report_dict, value_dict, current, options):
        # Don't display an aml report line (except the header) with all zero amounts.
        all_zero = all(
            self.env.company.currency_id.is_zero(value_dict[f])
            for f in ['period0', 'period1', 'period2', 'period3', 'period4', 'period5', 'period6', 'period7']
        ) and not value_dict.get('__count')
        return super()._show_line(report_dict, value_dict, current, options) and not all_zero

    def _format_total_line(self, res, value_dict, options):
        res['name'] = _('Total')
        res['colspan'] = len(self._get_column_details(options)) - 9
        res['columns'] = res['columns'][res['colspan']-1:]

    def _append_grouped(self, lines, current, line_dict, value_getters, value_formatters, options, hidden_lines):
        """Append the current line and all of its children recursively.

        :param lines (list<dict>): the list of report lines to send to the client
        :param current (list<tuple>): list of tuple(grouping_key, id)
        :param line_dict: the current hierarchy to unpack
        :param value_getters (list<function>): list of getter to retrieve each column's data.
            The parameter passed to the getter is the result of the read_group
        :param value_formatters (list<functions>): list of the value formatters.
            The parameter passed to the setter is the result of the getter.
        :param options (dict): report options.
        :param hidden_lines (dict): mapping between the lines hidden and their parent.
        """
        if line_dict['values'].get('__count', 1) == 0:
            return

        line = self._format_line(line_dict['values'], value_getters, value_formatters, current, options)
        if line['parent_id'] in hidden_lines:
            line['parent_id'] = hidden_lines[line['parent_id']]

        if self._show_line(line, line_dict['values'], current, options):
            lines.append(line)
        else:
            hidden_lines[line['id']] = hidden_lines.get('parent_id') or line['parent_id']
        if line not in lines:
            lines.append(line)
        # Add children recursively
        for key in line_dict['children']:
            self._append_grouped(
                lines=lines,
                current=current + [key],
                line_dict=line_dict['children'][key],
                value_getters=value_getters,
                value_formatters=value_formatters,
                options=options,
                hidden_lines=hidden_lines,
            )

        # Handle load more
        offset = line['offset'] = len(line_dict['children']) + int(options.get('lines_offset', 0))
        if (
            current and self._get_hierarchy_details(options)[len(current)-1].lazy
            and len(line_dict['children']) >= self.MAX_LINES and line_dict['children']
        ):
            load_more_line = self._get_load_more_line(
                line_dict=line_dict,
                value_getters=value_getters,
                value_formatters=value_formatters,
                current=current,
                options=options,
                offset=offset,
            )
            lines.append(load_more_line)

        # Handle section total line
        if (
            current and self._get_hierarchy_details(options)[len(current)-1].section_total
            and line_dict['children']
            and lines[-1] != line
        ):
            total_line = self._format_line(
                value_dict=line_dict['values'],
                value_getters=value_getters,
                value_formatters=value_formatters,
                current=current,
                options=options,
                total=True,
            )
            if self._show_line(total_line, line_dict['values'], current, options):
                lines.append(total_line)


# class ReportAgedPartnerBalance(models.AbstractModel):
#
#     _inherit = 'report.account.report_agedpartnerbalance'
#     # _description = 'Aged Partner Balance Report'
#
#     def _get_partner_move_lines(self, account_type, date_from, target_move, period_length):
#         # This method can receive the context key 'include_nullified_amount' {Boolean}
#         # Do an invoice and a payment and unreconcile. The amount will be nullified
#         # By default, the partner wouldn't appear in this report.
#         # The context key allow it to appear
#         # In case of a period_length of 30 days as of 2019-02-08, we want the following periods:
#         # Name       Stop         Start
#         # 1 - 30   : 2019-02-07 - 2019-01-09
#         # 31 - 60  : 2019-01-08 - 2018-12-10
#         # 61 - 90  : 2018-12-09 - 2018-11-10
#         # 91 - 120 : 2018-11-09 - 2018-10-11
#         # +120     : 2018-10-10
#         ctx = self._context
#         periods = {}
#         date_from = fields.Date.from_string(date_from)
#         start = date_from
#         for i in range(7)[::-1]:
#             stop = start - relativedelta(days=period_length)
#             period_name = str((7-(i+1)) * period_length + 1) + '-' + str((7-i) * period_length)
#             period_stop = (start - relativedelta(days=1)).strftime('%Y-%m-%d')
#             if i == 0:
#                 period_name = '+' + str(6 * period_length)
#             periods[str(i)] = {
#                 'name': period_name,
#                 'stop': period_stop,
#                 'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
#             }
#             start = stop
#
#         res = []
#         total = []
#         partner_clause = ''
#         cr = self.env.cr
#         user_company = self.env.company
#         user_currency = user_company.currency_id
#         company_ids = self._context.get('company_ids') or [user_company.id]
#         move_state = ['draft', 'posted']
#         if target_move == 'posted':
#             move_state = ['posted']
#         arg_list = (tuple(move_state), tuple(account_type), date_from,)
#         if 'partner_ids' in ctx:
#             if ctx['partner_ids']:
#                 partner_clause = 'AND (l.partner_id IN %s)'
#                 arg_list += (tuple(ctx['partner_ids'].ids),)
#             else:
#                 partner_clause = 'AND l.partner_id IS NULL'
#         if ctx.get('partner_categories'):
#             partner_clause += 'AND (l.partner_id IN %s)'
#             partner_ids = self.env['res.partner'].search([('category_id', 'in', ctx['partner_categories'].ids)]).ids
#             arg_list += (tuple(partner_ids or [0]),)
#         arg_list += (date_from, tuple(company_ids))
#
#         query = '''
#             SELECT DISTINCT l.partner_id, res_partner.name AS name, UPPER(res_partner.name) AS UPNAME, CASE WHEN prop.value_text IS NULL THEN 'normal' ELSE prop.value_text END AS trust
#             FROM account_move_line AS l
#               LEFT JOIN res_partner ON l.partner_id = res_partner.id
#               LEFT JOIN ir_property prop ON (prop.res_id = 'res.partner,'||res_partner.id AND prop.name='trust' AND prop.company_id=%s),
#               account_account, account_move am
#             WHERE (l.account_id = account_account.id)
#                 AND (l.move_id = am.id)
#                 AND (am.state IN %s)
#                 AND (account_account.internal_type IN %s)
#                 AND (
#                         l.reconciled IS NOT TRUE
#                         OR EXISTS (
#                             SELECT id FROM account_partial_reconcile where max_date > %s
#                             AND (credit_move_id = l.id OR debit_move_id = l.id)
#                         )
#                     )
#                     ''' + partner_clause + '''
#                 AND (l.date <= %s)
#                 AND l.company_id IN %s
#             ORDER BY UPPER(res_partner.name)
#             '''
#         arg_list = (self.env.company.id,) + arg_list
#         cr.execute(query, arg_list)
#
#         partners = cr.dictfetchall()
#         # put a total of 0
#         for i in range(9):
#             total.append(0)
#
#         # Build a string like (1,2,3) for easy use in SQL query
#         partner_ids = [partner['partner_id'] for partner in partners]
#         lines = dict((partner['partner_id'], []) for partner in partners)
#         if not partner_ids:
#             return [], [], {}
#
#         lines[False] = []
#         # Use one query per period and store results in history (a list variable)
#         # Each history will contain: history[1] = {'<partner_id>': <partner_debit-credit>}
#         history = []
#         for i in range(7):
#             args_list = (tuple(move_state), tuple(account_type), tuple(partner_ids),)
#             dates_query = '(COALESCE(l.date_maturity,l.date)'
#
#             if periods[str(i)]['start'] and periods[str(i)]['stop']:
#                 dates_query += ' BETWEEN %s AND %s)'
#                 args_list += (periods[str(i)]['start'], periods[str(i)]['stop'])
#             elif periods[str(i)]['start']:
#                 dates_query += ' >= %s)'
#                 args_list += (periods[str(i)]['start'],)
#             else:
#                 dates_query += ' <= %s)'
#                 args_list += (periods[str(i)]['stop'],)
#             args_list += (date_from, tuple(company_ids))
#
#             query = '''SELECT l.id
#                     FROM account_move_line AS l, account_account, account_move am
#                     WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
#                         AND (am.state IN %s)
#                         AND (account_account.internal_type IN %s)
#                         AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
#                         AND ''' + dates_query + '''
#                     AND (l.date <= %s)
#                     AND l.company_id IN %s
#                     ORDER BY COALESCE(l.date_maturity, l.date)'''
#             cr.execute(query, args_list)
#             partners_amount = {}
#             aml_ids = [x[0] for x in cr.fetchall()]
#             # prefetch the fields that will be used; this avoid cache misses,
#             # which look up the cache to determine the records to read, and has
#             # quadratic complexity when the number of records is large...
#             move_lines = self.env['account.move.line'].browse(aml_ids)
#             move_lines._read(['partner_id', 'company_id', 'balance', 'matched_debit_ids', 'matched_credit_ids'])
#             move_lines.matched_debit_ids._read(['max_date', 'company_id', 'amount'])
#             move_lines.matched_credit_ids._read(['max_date', 'company_id', 'amount'])
#             for line in move_lines:
#                 partner_id = line.partner_id.id or False
#                 if partner_id not in partners_amount:
#                     partners_amount[partner_id] = 0.0
#                 line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from, round = False)
#                 if user_currency.is_zero(line_amount):
#                     continue
#                 for partial_line in line.matched_debit_ids:
#                     if partial_line.max_date <= date_from:
#                         line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from, round = False)
#                 for partial_line in line.matched_credit_ids:
#                     if partial_line.max_date <= date_from:
#                         line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from, round = False)
#
#                 line_amount = user_currency.round(line_amount)
#                 if not self.env.company.currency_id.is_zero(line_amount):
#                     partners_amount[partner_id] += line_amount
#                     lines.setdefault(partner_id, [])
#                     lines[partner_id].append({
#                         'line': line,
#                         'amount': line_amount,
#                         'period': i + 1,
#                         })
#             history.append(partners_amount)
#
#         # This dictionary will store the not due amount of all partners
#         undue_amounts = {}
#         query = '''SELECT l.id
#                 FROM account_move_line AS l, account_account, account_move am
#                 WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
#                     AND (am.state IN %s)
#                     AND (account_account.internal_type IN %s)
#                     AND (COALESCE(l.date_maturity,l.date) >= %s)\
#                     AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
#                 AND (l.date <= %s)
#                 AND l.company_id IN %s
#                 ORDER BY COALESCE(l.date_maturity, l.date)'''
#         cr.execute(query, (tuple(move_state), tuple(account_type), date_from, tuple(partner_ids), date_from, tuple(company_ids)))
#         aml_ids = cr.fetchall()
#         aml_ids = aml_ids and [x[0] for x in aml_ids] or []
#         for line in self.env['account.move.line'].browse(aml_ids):
#             partner_id = line.partner_id.id or False
#             if partner_id not in undue_amounts:
#                 undue_amounts[partner_id] = 0.0
#             line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from, round = False)
#             if user_currency.is_zero(line_amount):
#                 continue
#             for partial_line in line.matched_debit_ids:
#                 if partial_line.max_date <= date_from:
#                     line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from, round = False)
#             for partial_line in line.matched_credit_ids:
#                 if partial_line.max_date <= date_from:
#                     line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from, round = False)
#             line_amount = user_currency.round(line_amount)
#             if not self.env.company.currency_id.is_zero(line_amount):
#                 undue_amounts[partner_id] += line_amount
#                 lines.setdefault(partner_id, [])
#                 lines[partner_id].append({
#                     'line': line,
#                     'amount': line_amount,
#                     'period': 6,
#                 })
#
#         for partner in partners:
#             if partner['partner_id'] is None:
#                 partner['partner_id'] = False
#             at_least_one_amount = False
#             values = {}
#             undue_amt = 0.0
#             if partner['partner_id'] in undue_amounts:  # Making sure this partner actually was found by the query
#                 undue_amt = undue_amounts[partner['partner_id']]
#
#             # print (total, len(total))
#             total[8] = total[8] + undue_amt
#             values['direction'] = undue_amt
#             if not float_is_zero(values['direction'], precision_rounding=self.env.company.currency_id.rounding):
#                 at_least_one_amount = True
#
#             for i in range(7):
#                 during = False
#                 if partner['partner_id'] in history[i]:
#                     during = [history[i][partner['partner_id']]]
#                 # Adding counter
#                 total[(i)] = total[(i)] + (during and during[0] or 0)
#                 values[str(i)] = during and during[0] or 0.0
#                 if not float_is_zero(values[str(i)], precision_rounding=self.env.company.currency_id.rounding):
#                     at_least_one_amount = True
#             values['total'] = sum([values['direction']] + [values[str(i)] for i in range(7)])
#             # Add for total
#             total[(i + 1)] += values['total']
#             values['partner_id'] = partner['partner_id']
#             if partner['partner_id']:
#                 name = partner['name'] or ''
#                 values['name'] = len(name) >= 45 and not self.env.context.get('no_format') and name[0:41] + '...' or name
#                 values['trust'] = partner['trust']
#             else:
#                 values['name'] = _('Unknown Partner')
#                 values['trust'] = False
#
#             if at_least_one_amount or (self._context.get('include_nullified_amount') and lines[partner['partner_id']]):
#                 res.append(values)
#         return res, total, lines
