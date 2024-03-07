from odoo import models, fields, api, _


class SaleOrderLineWizard(models.TransientModel):
    _name = 'sale.order.line.wizard'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Sale Order Line Wizard'

    order_line_ids = fields.One2many('sale.order.line.wizard.line', 'wizard_id', string='Sale Order Lines')
    total = fields.Float(string="Total", compute='depends_total')
    is_hide_confirm_button = fields.Boolean(default=False, compute="_compute_is_hide_confirm_button")

    def _compute_is_hide_confirm_button(self):
        for wizard in self:
            active_id = wizard._context.get('active_id')
            if active_id:
                sale_order_state = wizard.env['sale.order'].browse(active_id).state
                if sale_order_state == 'sale':
                    wizard.is_hide_confirm_button = True
                else:
                    wizard.is_hide_confirm_button = False

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
        return {'type': 'ir.actions.act_window_close'}


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
