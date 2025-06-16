from odoo import models, fields, api, _


class SaleOrderLineWizard(models.TransientModel):
    _name = 'sale.order.line.wizard'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Sale Order Line Wizard'

    order_line_ids = fields.One2many('sale.order.line.wizard.line', 'wizard_id', string='Sale Order Lines')
    total = fields.Float(string="Total", compute='depends_total')
    is_hide_confirm_button = fields.Boolean(default=False, compute="_compute_is_hide_confirm_button")
    is_hide_approve_button = fields.Boolean(default=False)
    is_hide_send_for_approval = fields.Boolean(default=False)

    def _compute_is_hide_confirm_button(self):
        for wizard in self:
            active_id = wizard._context.get('active_id')
            if active_id:
                sale_order = wizard.env['sale.order'].browse(active_id)
                sale_order_state = sale_order.state
                if not self.env.user.has_group('aspl_sale_workflow.group_sales_rep') or \
                    sale_order_state not in ['draft', 'sent', 'approved'] or (sale_order.partner_credit_sale_limit and (not sale_order.is_order_approved)):
                    wizard.is_hide_confirm_button = True
                else:
                    wizard.is_hide_confirm_button = False

                if not self.env.user.has_group('aspl_sale_workflow.group_supervisor') or \
                    sale_order.state not in ['sup_approval']:
                    wizard.is_hide_approve_button = True
                else:
                    wizard.is_hide_approve_button = False

                if not self.env.user.has_group('aspl_sale_workflow.group_sales_rep') or \
                    sale_order_state not in ['draft', 'sent'] or not sale_order.partner_credit_sale_limit or \
                        not sale_order.enable_send_for_approval:
                            self.is_hide_send_for_approval = True

    @api.depends('order_line_ids')
    def depends_total(self):
        total_1 = 0
        data = self.env.context.get('active_id')
        if data:
            record = self.env['sale.order'].browse(data)
            for price in record.order_line:
                total_1 = total_1 + price.price_subtotal
            self.total = total_1

    def approve_so_order(self):
        data = self.env.context.get('active_id')
        if data:
            record = self.env['sale.order'].browse(data)
            record.is_approved = True
            record.is_order_approved = record.is_sale_limit_approved = record.is_credit_limit_approved = True
            record.state = 'approved'

    def create_active_so_order(self):
        return {
            'name': _('Schedule Activity'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'view_id': self.env.ref('mail.mail_activity_view_form_popup').id,
            'res_model': 'mail.activity',
            'context': {
                'default_res_id': self._context.get('active_id'),
                'default_res_model': self._context.get('active_model'),
            },
            'target': 'new',
        }

    def confirm_so_order(self):
        data = self.env.context.get('active_id')
        if data:
            sale_order = self.env['sale.order'].browse(data)
            if sale_order:
                sale_order.action_confirm()
                if sale_order.partner_credit_sale_limit and (not sale_order.is_sale_limit_approved or not sale_order.is_credit_limit_approved):
                    msg = ""
                    if not sale_order.is_sale_limit_approved and sale_order.is_credit_limit_approved:
                        msg = "Sale limit is exceeded. You can't confirm this order."
                    elif not sale_order.is_credit_limit_approved and sale_order.is_sale_limit_approved:
                        msg = "Credit limit is exceeded. You can't confirm this order."
                    elif not sale_order.is_sale_limit_approved and not sale_order.is_credit_limit_approved:
                        msg = "Both Sale and Credit limit is exceeded. You can't confirm this order."
                    return {
                        'name': _('Validation Error'),
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'warning.wizard',
                        'context': {'msg': msg, 'sale_order_id': data},
                        'target': 'new',
                    }
        return {'type': 'ir.actions.act_window_close'}

    def send_for_approval(self):
        data = self.env.context.get('active_id')
        if data:
            sale_order = self.env['sale.order'].browse(data)
            sale_order.state = 'sup_approval'
            sale_order.is_credit_limit_approved = sale_order.is_sale_limit_approved = False

class SaleOrderLineWizardLine(models.TransientModel):
    _name = 'sale.order.line.wizard.line'
    _description = 'Sale Order Line Wizard Line'

    wizard_id = fields.Many2one('sale.order.line.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    product_uom = fields.Float(string='UoM')
    product_uom = fields.Many2one('uom.uom', string='UoM')
    price_unit = fields.Float(string='Unit Price')
    price_subtotal = fields.Float(string='Subtotal')
    product_uom_qty = fields.Float(string='Quantity')
