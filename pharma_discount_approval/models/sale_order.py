
from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_discount = fields.Boolean(string='Discount', copy=False)

    def action_confirm(self):
        res = super().action_confirm()
        if not self.env.user.has_group('base.group_erp_manager'):
            if self.is_discount:
                return res
            else:
                orders = self.order_line.filtered(lambda l: l.discount > 0.0)
                disc_order_line = self.order_line.filtered(lambda l: l.product_id.name == 'Discount')
                if disc_order_line:
                    order_lines = self.order_line.filtered(lambda l: l.id != disc_order_line.id)
                    if self.sales_rep_id.disc_type == 'fix_amount':
                        disc = self.sales_rep_id.max_disc_amt
                        if abs(disc_order_line.price_subtotal) >= disc:
                            self.is_discount = False
                            raise UserError('You have exceeded the maximum limit of discount. '
                                            'Please ask other Sales Representative or Manager to approve.')
                    else:
                        discounted_amount = sum(order_lines.mapped('price_subtotal'))
                        order_line_disc_percent = discounted_amount / disc_order_line.price_subtotal
                        if abs(order_line_disc_percent) >= self.sales_rep_id.max_disc_pt:
                            self.is_discount = False
                            raise UserError('You have exceeded the maximum limit of discount. '
                                            'Please ask other Sales Representative or Manager to approve.')

                if orders:
                    discount = sum(orders.mapped('discount'))
                    price = sum(orders.mapped('price_subtotal'))
                    if self.sales_rep_id.disc_type == 'fix_amount':
                        discount_value = price / discount
                    else:
                        discount_value = self.sales_rep_id.max_disc_pt
                    if discount >= discount_value:
                        self.is_discount = False
                        raise UserError('You have exceeded the maximum limit of discount. '
                                        'Please ask other Sales Representative or Manager to approve.')
        return res

    def action_approve_discount(self):
        if not self.env.user.has_group('base.group_erp_manager'):
            if self.env.user == self.sales_rep_id:
                raise UserError('You are not allowed to approve the discount.')
            else:
                self.is_discount = True
        else:
            self.is_discount = True
