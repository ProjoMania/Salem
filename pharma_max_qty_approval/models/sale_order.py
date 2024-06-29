from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('in_approved', 'In Approved')],
                             ondelete={'in_approved': 'cascade'})
    supervisor_approval = fields.Boolean(string="Supervisor Approval", invisible=1)
    approval = fields.Boolean(string="Approval", invisible=1)

    def action_approve(self):
        if self.sales_rep_id:
            if self.sales_rep_id.supervisor_id or self.sales_rep_id.manager_id:
                self.supervisor_approval = True
                if not self.approval:
                    self.state = 'draft'
                else:
                    self.state = 'sale'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def write(self, vals):
        res = super().write(vals)
        if vals.get('product_uom_qty'):
            if 'product_uom_qty' in vals and self.order_id.state == 'sale':
                self.order_id.approval = True
                self.order_id.state = 'in_approved'
            elif vals.get('product_uom_qty') > self.order_id.sales_rep_id.max_qty:
                self.order_id.state = 'in_approved'
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_uom_qty'):
                order_id = self.env['sale.order'].browse(vals.get('order_id'))
                if vals.get('product_uom_qty') >= order_id.sales_rep_id.max_qty:
                    order_id.state = 'in_approved'
                    order_id.approval = False
        return super().create(vals_list)
