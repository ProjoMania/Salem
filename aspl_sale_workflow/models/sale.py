from odoo import api, fields, models, _, Command
import math
from datetime import datetime, timedelta
import base64
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    workflow_process = fields.Selection(
        [('default', 'Default Workflow'),
         ('workflow_2', 'Workflow 2'),
         ('workflow_3', 'Workflow 3')],
        string='Workflow Process',
        default='default'
    )
    pricelist_readonly = fields.Boolean(compute='_compute_pricelist_readonly')
    is_approval_needed = fields.Boolean(compute='_compute_advance_approval')

    enable_multiple_workflows = fields.Boolean(
        related="company_id.enable_multiple_workflows")
    # This field is related to aspl_sale_order_quick_preview module flow
    is_approved = fields.Boolean(string="Is Approved")

    partner_credit_sale_limit = fields.Boolean(
        related="partner_id.credit_sale_limit")
    is_credit_limit_approved = fields.Boolean(
        string="Credit Limit Approved", default=False)
    is_sale_limit_approved = fields.Boolean(
        string="Sale Limit Approved", default=False)
    state = fields.Selection(selection_add=[('sup_approval', 'Waiting for Approval'),
                                            ('approved', 'Approved')])

    is_order_approved = fields.Boolean(
        string="Is Order Approved", default=True)
    enable_send_for_approval = fields.Boolean(
        string="Enable Send for Approval", default=False)

    @api.depends('order_line', 'partner_id')
    def _compute_advance_approval(self):
        for rec in self:
            if not rec.order_line:
                rec.is_approval_needed = False
                continue

            price_list_check = any(
                (line.product_uom_qty * line.price_unit) /
                (line.product_uom_qty +
                 (math.floor(line.product_uom_qty * pricelist_item.foc_by_vendor / 100) if pricelist_item else 0) +
                 (math.floor(line.product_uom_qty *
                  pricelist_item.foc_by_company / 100) if pricelist_item else 0)
                 ) < pricelist_item.net_price
                for line in rec.order_line.filtered(lambda l: not l.is_foc)
                if (pricelist_item := rec.pricelist_id.item_ids.filtered(
                    lambda l: l.product_id.id == line.product_id.id or l.product_tmpl_id.id == line.product_template_id.id
                ))
            )
            rec.is_approval_needed = price_list_check

    @api.depends('company_id.enable_multiple_workflows')
    def _compute_pricelist_readonly(self):
        for order in self:
            order.pricelist_readonly = order.enable_multiple_workflows

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if not self.enable_multiple_workflows:
            self.workflow_process = 'default'

    # Even if partner or company changes, price list should be updated
    @api.onchange('workflow_process', 'partner_id', 'company_id')
    def _onchange_workflow_process(self):
        if self.workflow_process == 'default':
            workflow_type = 'default'
        elif self.workflow_process == 'workflow_2':
            workflow_type = 'workflow_2'
        elif self.workflow_process == 'workflow_3':
            workflow_type = 'workflow_3'
        else:
            workflow_type = 'default'
            # workflow_type = 'workflow_3'
        self.pricelist_id = self.env['product.pricelist'].search([
            ('workflow_process', '=', workflow_type)
        ], limit=1).id

    @api.onchange('pricelist_id', 'order_line')
    def _onchange_pricelist_id(self):
        main_product_lines = {}
        for line in self.order_line:
            if not line.is_foc:
                main_product_lines.update(
                    {line.product_id.id: line.product_uom_qty})

        self.order_line = [fields.Command.clear()]
        if self.pricelist_id and self.pricelist_id.workflow_process == 'workflow_3':
            for product_id, qty in main_product_lines.items():
                pricelist_item_id = self.pricelist_id.item_ids.filtered(
                    lambda l: l.product_id.id == product_id or l.product_tmpl_id.id == product_id)

                self.order_line = [(0, 0, {
                    'product_id': product_id,
                    'analytic_distribution': pricelist_item_id.analytic_distribution,
                    'product_uom_qty': qty,
                })]

                if pricelist_item_id:
                    foc_vendor_qty = math.floor(
                        qty * pricelist_item_id.foc_by_vendor / 100)
                    foc_company_qty = math.floor(
                        qty * pricelist_item_id.foc_by_company / 100)
                    if foc_vendor_qty > 0:
                        self.order_line = [(0, 0, {
                            'product_id': product_id,
                            'product_uom_qty': foc_vendor_qty,
                            'price_unit': 0.0,
                            'analytic_distribution': pricelist_item_id.analytic_distribution_for_vendor,
                            'is_foc': True,
                            'workflow_process': 'workflow_3',
                        })]

                    if foc_company_qty > 0:
                        self.order_line = [(0, 0, {
                            'product_id': product_id,
                            'product_uom_qty': foc_company_qty,
                            'price_unit': 0.0,
                            'analytic_distribution': pricelist_item_id.analytic_distribution_for_company,
                            'is_foc': True,
                            'workflow_process': 'workflow_3',
                        })]
        elif self.pricelist_id and self.pricelist_id.workflow_process == 'workflow_2':
            for product_id, qty in main_product_lines.items():
                pricelist_item_id = self.pricelist_id.item_ids.filtered(
                    lambda l: l.product_id.id == product_id or l.product_tmpl_id.id == product_id)
                self.order_line = [(0, 0, {
                    'product_id': product_id,
                    'analytic_distribution': pricelist_item_id.analytic_distribution,
                    'product_uom_qty': qty,
                })]

                if pricelist_item_id:
                    foc_vendor_qty = math.floor(
                        qty * pricelist_item_id.foc_by_vendor / 100)
                    if foc_vendor_qty > 0:
                        self.order_line = [(0, 0, {
                            'product_id': product_id,
                            'product_uom_qty': foc_vendor_qty,
                            'price_unit': 0.0,
                            'analytic_distribution': pricelist_item_id.analytic_distribution_for_vendor,
                            'is_foc': True,
                            'workflow_process': 'workflow_2',
                        })]
        else:
            for product_id, qty in main_product_lines.items():
                self.order_line = [(0, 0, {
                    'product_id': product_id,
                    'product_uom_qty': qty,
                })]

    def check_credit_limit(self):
        self.is_credit_limit_approved = True
        if self.is_sale_limit_approved:
            self.is_order_approved = True
            self.state = 'approved'

    def check_sale_limit(self):
        self.is_sale_limit_approved = True
        if self.is_credit_limit_approved:
            self.is_order_approved = True
            self.state = 'approved'

    def send_for_approval(self):
        self.state = 'sup_approval'
        self.is_credit_limit_approved = self.is_sale_limit_approved = False

    def action_confirm(self):
        if self.partner_credit_sale_limit:
            if not self.is_credit_limit_approved:
                total_invoiced_amount = sum(self.partner_id.invoice_ids.filtered(
                    lambda invoice: invoice.move_type == 'out_invoice').mapped('amount_total'))
                if total_invoiced_amount < self.partner_id.credit_limit:
                    self.is_credit_limit_approved = True
            if not self.is_sale_limit_approved:
                if self.amount_total < self.partner_id.sales_limit:
                    self.is_sale_limit_approved = True

            if self.is_credit_limit_approved and self.is_sale_limit_approved:
                self.is_order_approved = True
                self.state = 'draft'
                return super(SaleOrder, self).action_confirm()
            else:
                if not self.is_sale_limit_approved and self.is_credit_limit_approved:
                    msg = "Sale limit is exceeded. You can't confirm this order."
                elif not self.is_credit_limit_approved and self.is_sale_limit_approved:
                    msg = "Credit limit is exceeded. You can't confirm this order."
                else:
                    msg = "Both Sale and Credit limit is exceeded. You can't confirm this order."
                # raise warning
                return {
                    'name': _('Validation Error'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'warning.wizard',
                    'context': {'msg': msg},
                    'target': 'new',
                }
                # self.enable_send_for_approval = True
                # self.is_order_approved = False
        else:
            self.state = 'draft'
            return super(SaleOrder, self).action_confirm()

    # Cron method
    def _send_daily_so_report(self):
        order_date_start = datetime.now().replace(
            hour=0, minute=0, second=0) + timedelta(days=-1)
        order_date_end = datetime.now().replace(
            hour=23, minute=59, second=59) + timedelta(days=-1)
        domain = [('create_date', '>=', order_date_start),
                  ('create_date', '<=', order_date_end)]
        sale_orders = self.env['sale.order'].search(domain)
        report_template_id = self.env['ir.actions.report']._render_qweb_pdf(
            'aspl_sale_workflow.daily_sale_report', sale_orders.ids)
        report_data_record = base64.b64encode(report_template_id[0])

        ir_values = {
            'name': "Daily Sales Report",
            'type': 'binary',
            'datas': report_data_record,
            'store_fname': report_data_record,
            'mimetype': 'application/x-pdf',
        }
        report_id = self.env['ir.attachment'].create(ir_values)

        mail_ids = self.env['res.users'].search(
            [('receive_daily_SO_reports', '=', True), ('email', '!=', False)]).mapped('email_formatted')
        email_values = {
            'email_to': ','.join(mail_ids)
        }
        mail_template = self.env.ref(
            'aspl_sale_workflow.daily_sale_report_mail_temp')
        mail_template.attachment_ids = [(6, 0, [report_id.id])]
        mail_template.send_mail(self.id, force_send=True,
                                email_values=email_values)

    # preview method
    def button_quick_preview(self):
        wizard = self.env['sale.order.line.wizard'].create({})
        for line in self.order_line:
            wizard_line = self.env['sale.order.line.wizard.line'].create({
                'wizard_id': wizard.id,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'product_uom_qty': line.product_uom_qty,
            })
        return {
            'name': _('Sale Order Lines'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('aspl_sale_workflow.view_sale_order_line_wizard_form').id,
            'res_model': 'sale.order.line.wizard',
            'res_id': wizard.id,
            'target': 'new',
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_foc = fields.Boolean(string='Is FOC Line')
    workflow_process = fields.Selection(
        [('default', 'Default Workflow'),
         ('workflow_2', 'Workflow 2'),
         ('workflow_3', 'Workflow 3')],
        string='Workflow Process',
        default='default'
    )
