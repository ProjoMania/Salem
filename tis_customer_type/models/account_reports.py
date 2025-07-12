from odoo import models, api, fields


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    def _init_options_partner(self, options, previous_options=None):
        # Always ensure selected_partner_categories is set to avoid KeyError in templates
        options['selected_partner_categories'] = []
        
        options['partner_categories'] = previous_options and previous_options.get('partner_categories') or []
        options['customer_type'] = previous_options and previous_options.get('customer_type') or []
        selected_partner_customer_type_ids = [int(cust_type) for cust_type in options['customer_type']]
        selected_partner_customer_type = selected_partner_customer_type_ids and self.env['customer.type'].browse(
            selected_partner_customer_type_ids) or self.env['res.partner.category']
        options['selected_customer_type'] = selected_partner_customer_type.mapped('name')
        return super()._init_options_partner(options, previous_options)

    def _init_filter_partner(self, options, previous_options=None):
        res = super()._init_filter_partner(options, previous_options)
        options['customer_type'] = previous_options and previous_options.get('customer_type') or []
        selected_partner_customer_type_ids = [int(cust_type) for cust_type in options['customer_type']]
        selected_partner_customer_type = selected_partner_customer_type_ids and self.env['customer.type'].browse(
            selected_partner_customer_type_ids) or self.env['res.partner.category']
        options['selected_customer_type'] = selected_partner_customer_type.mapped('name')
        return res

    @api.model
    def _get_options_partner_domain(self, options):
        res = super()._get_options_partner_domain(options)
        if options.get('customer_type'):
            partner_customer_ids = [int(category) for category in options['customer_type']]
            res.append(('partner_id.customer_type', 'in', partner_customer_ids))
        return res

    def get_report_informations(self, options):
        '''
        return a dictionary of informations that will be needed by the js widget, manager_id, footnotes, html of report and searchview, ...
        '''
        options = self._get_options(options)
        self = self.with_context(self._set_context(
            options))  # For multicompany, when allowed companies are changed by options (such as aggregare_tax_unit)

        searchview_dict = {'options': options, 'context': self.env.context}
        # Check if report needs analytic
        if options.get('analytic_accounts') is not None:
            options['selected_analytic_account_names'] = [self.env['account.analytic.account'].browse(int(account)).name
                                                          for account in options['analytic_accounts']]
        if options.get('analytic_tags') is not None:
            options['selected_analytic_tag_names'] = [self.env['account.account.tag'].browse(int(tag)).name for tag in
                                                      options['analytic_tags']]
        if options.get('partner'):
            options['selected_partner_ids'] = [self.env['res.partner'].browse(int(partner)).name for partner in
                                               options['partner_ids']]
            options['selected_partner_categories'] = [self.env['res.partner.category'].browse(int(category)).name for
                                                      category in (options.get('partner_categories') or [])]
            options['selected_customer_type'] = [self.env['customer.type'].browse(int(cust_type)).name for cust_type in
                                                 (options.get('customer_type') or [])]

        # Check whether there are unposted entries for the selected period or not (if the report allows it)
        if options.get('date') and options.get('all_entries') is not None:
            date_to = options['date'].get('date_to') or options['date'].get('date') or fields.Date.today()
            period_domain = [('state', '=', 'draft'), ('date', '<=', date_to)]
            options['unposted_in_period'] = bool(self.env['account.move'].search_count(period_domain))

        report_manager = self._get_report_manager(options)
        info = {'options': options,
                'context': self.env.context,
                'report_manager_id': report_manager.id,
                'footnotes': [{'id': f.id, 'line': f.line, 'text': f.text} for f in report_manager.footnotes_ids],
                'buttons': self._get_reports_buttons_in_sequence(options),
                'main_html': self.get_html(options),
                'searchview_html': self.env['ir.ui.view']._render_template(
                    self._get_templates().get('search_template', 'account_report.search_template'),
                    values=searchview_dict),
                }
        return info
