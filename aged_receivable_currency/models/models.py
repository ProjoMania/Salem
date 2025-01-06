# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class AccountReport(models.Model):
#     _inherit = 'account.report'

#     def _build_column_dict(
#             self, col_value, col_data,
#             options=None, currency=False, digits=1,
#             column_expression=None, has_sublines=False,
#             report_line_id=None,
#     ):
#         currency_symbol = self.env.company.currency_id.symbol if options.get('multi_currency') else None
#         currency = self.env['res.currency'].browse(87)
#         if currency or currency_symbol:
#             print(currency)
#             print(currency_symbol)
#         # Empty column
#         if col_value is None and col_data is None:
#             return {}

#         col_data = col_data or {}
#         column_expression = column_expression or self.env['account.report.expression']
#         options = options or {}

#         blank_if_zero = column_expression.blank_if_zero or col_data.get('blank_if_zero', False)
#         figure_type = column_expression.figure_type or col_data.get('figure_type', 'string')

#         return {
#             'auditable': col_value is not None and column_expression.auditable,
#             'blank_if_zero': blank_if_zero,
#             'column_group_key': col_data.get('column_group_key'),
#             'currency': currency,
#             'currency_symbol': self.env.company.currency_id.symbol if options.get('multi_currency') else None,
#             'digits': digits,
#             'expression_label': col_data.get('expression_label'),
#             'figure_type': figure_type,
#             'green_on_positive': column_expression.green_on_positive,
#             'has_sublines': has_sublines,
#             'is_zero': col_value is None or (
#                 isinstance(col_value, (int, float))
#                 and figure_type in ('float', 'integer', 'monetary')
#                 and self.is_zero(col_value, currency=currency, figure_type=figure_type, digits=digits)
#             ),
#             'name': self._format_value(options, col_value, currency=currency, blank_if_zero=blank_if_zero, figure_type=figure_type, digits=digits),
#             'no_format': col_value,
#             'report_line_id': report_line_id,
#             'sortable': col_data.get('sortable', False),
#         }


    # def get_report_information(self, options):
    #     res = super(AccountReport, self).get_report_information(options)
    #     # Create a file and write the 'res' data to it
    #     # Add the file 'res_data.txt' to the directory '/home/moh'
    #     with open('/home/moh/res_data.txt', 'w') as f:
    #         f.write(str(res.get('lines')))

    #     return res

    # def _get_lines(self, options, all_column_groups_expression_totals=None, warnings=None):
        # self.ensure_one()

        # if warnings is not None:
        #     self._generate_common_warnings(options, warnings)

        # if options['report_id'] != self.id:
        #     # Should never happen; just there to prevent BIG issues and directly spot them
        #     raise UserError(_("Inconsistent report_id in options dictionary. Options says %s; report is %s.", options['report_id'], self.id))

        # # Necessary to ensure consistency of the data if some of them haven't been written in database yet
        # self.env.flush_all()

        # # Merge static and dynamic lines in a common list
        # if all_column_groups_expression_totals is None:
        #     all_column_groups_expression_totals = self._compute_expression_totals_for_each_column_group(
        #         self.line_ids.expression_ids,
        #         options,
        #         warnings=warnings,
        #     )

        # dynamic_lines = self._get_dynamic_lines(options, all_column_groups_expression_totals, warnings=warnings)

        # lines = []
        # line_cache = {} # {report_line: report line dict}
        # hide_if_zero_lines = self.env['account.report.line']

        # # There are two types of lines:
        # # - static lines: the ones generated from self.line_ids
        # # - dynamic lines: the ones generated from a call to the functions referred to by self.dynamic_lines_generator
        # # This loops combines both types of lines together within the lines list
        # for line in self.line_ids: # _order ensures the sequence of the lines
        #     # Inject all the dynamic lines whose sequence is inferior to the next static line to add
        #     while dynamic_lines and line.sequence > dynamic_lines[0][0]:
        #         lines.append(dynamic_lines.pop(0)[1])
        #     parent_generic_id = line_cache[line.parent_id]['id'] if line.parent_id else None # The parent line has necessarily been treated in a previous iteration
        #     line_dict = self._get_static_line_dict(options, line, all_column_groups_expression_totals, parent_id=parent_generic_id)
        #     line_cache[line] = line_dict

        #     if line.hide_if_zero:
        #         hide_if_zero_lines += line

        #     lines.append(line_dict)

        # for dummy, left_dynamic_line in dynamic_lines:
        #     lines.append(left_dynamic_line)

        # # Manage growth comparison
        # if self._display_growth_comparison(options):
        #     for line in lines:
        #         first_value, second_value = line['columns'][0]['no_format'], line['columns'][1]['no_format']

        #         if not first_value and not second_value:  # For layout lines and such, with no values
        #             line['growth_comparison_data'] = {'name': '0.0%', 'growth': 0}
        #         else:
        #             green_on_positive = True
        #             model, line_id = self._get_model_info_from_id(line['id'])

        #             if model == 'account.report.line' and line_id:
        #                 report_line = self.env['account.report.line'].browse(line_id)
        #                 compared_expression = report_line.expression_ids.filtered(
        #                     lambda expr: expr.label == line['columns'][0]['expression_label']
        #                 )
        #                 green_on_positive = compared_expression.green_on_positive

        #             line['growth_comparison_data'] = self._compute_growth_comparison_column(
        #                 options, first_value, second_value, green_on_positive=green_on_positive
        #             )

        # # Manage hide_if_zero lines:
        # # - If they have column values: hide them if all those values are 0 (or empty)
        # # - If they don't: hide them if all their children's column values are 0 (or empty)
        # # Also, hide all the children of a hidden line.
        # hidden_lines_dict_ids = set()
        # for line in hide_if_zero_lines:
        #     children_to_check = line
        #     current = line
        #     while current:
        #         children_to_check |= current
        #         current = current.children_ids

        #     all_children_zero = True
        #     hide_candidates = set()
        #     for child in children_to_check:
        #         child_line_dict_id = line_cache[child]['id']

        #         if child_line_dict_id in hidden_lines_dict_ids:
        #             continue
        #         elif all(col.get('is_zero', True) for col in line_cache[child]['columns']):
        #             hide_candidates.add(child_line_dict_id)
        #         else:
        #             all_children_zero = False
        #             break

        #     if all_children_zero:
        #         hidden_lines_dict_ids |= hide_candidates

        # lines[:] = filter(lambda x: x['id'] not in hidden_lines_dict_ids and x.get('parent_id') not in hidden_lines_dict_ids, lines)

        # # Create the hierarchy of lines if necessary
        # if options.get('hierarchy'):
        #     lines = self._create_hierarchy(lines, options)

        # # Handle totals below sections for static lines
        # lines = self._add_totals_below_sections(lines, options)

        # # Unfold lines (static or dynamic) if necessary and add totals below section to dynamic lines
        # lines = self._fully_unfold_lines_if_needed(lines, options)

        # if self.custom_handler_model_id:
        #     lines = self.env[self.custom_handler_model_name]._custom_line_postprocessor(self, options, lines, warnings=warnings)

        # return lines

