from odoo import models, fields, api, _


class WarningWizard(models.TransientModel):
    _name = 'warning.wizard'
    _description = 'Warning Wizard'

    msg = fields.Char(default=lambda self: self.env.context.get('msg'), readonly="1")

    def continue_process(self):
        order_id = self.env.context.get('sale_order_id') or self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(order_id)
        sale_order.enable_send_for_approval = True
        sale_order.is_order_approved = False
