
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_discount = fields.Boolean()
    show_discount_button = fields.Boolean(string="Show Discount Button")

    def approve_discount(self):
        if self.env.user.id == self.sales_rep_id.id:
            self.is_discount = False
            raise UserError('You are not allowed to approve this discount.'
                            'You need an approval from another Sales Representative.')
        else:
            self.is_discount = True
            self.show_discount_button = False


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        active_id = self.env['account.move'].browse(self._context.get('active_id'))
        res = super(AccountPaymentRegister, self).action_create_payments()
        if not self.env.user.has_group('base.group_erp_manager'):
            if active_id.is_discount:
                active_id.is_discount = False
                return res
            discount_payment_amt = 0
            if self.discount_type == 'fix_amount':
                discount_payment_amt = self.discount_amount
            elif self.discount_type == 'percentage':
                discount_payment_amt = self.discount_percentage * self.payment_difference / 100
            if active_id.sales_rep_id.disc_payment_type == 'fix_amount':
                discount_amt = active_id.sales_rep_id.max_payment_disc_amt
                if discount_payment_amt > discount_amt:
                    raise UserError(_('You have reached the maximum limit of Discount.'
                                      'Please create an activity to approve the discount from the invoice.'))
            else:
                discount_amt = active_id.sales_rep_id.max_payment_disc_pt
                if self.discount_percentage > discount_amt:
                    raise UserError(_('You have reached the maximum limit of Discount.'
                                      'Please create an activity to approve the discount from the invoice.'))
        else:
            return res

    @api.onchange('discount_amount', 'discount_percentage')
    def onchange_discount(self):
        active_id = self.env['account.move'].browse(self._context.get('active_id'))
        discount = 0
        discount_percent = 0
        if not self.env.user.has_group('base.group_erp_manager'):
            if self.discount_type == 'fix_amount':
                discount = self.discount_amount
            elif self.discount_type == 'percentage':
                discount = self.discount_percentage * self.payment_difference / 100
                discount_percent = self.discount_percentage
            if discount:
                if discount > active_id.sales_rep_id.max_payment_disc_amt:
                    if not active_id.is_discount:
                        active_id.show_discount_button = True
                else:
                    active_id.show_discount_button = False
            if discount_percent:
                if discount > active_id.sales_rep_id.max_payment_disc_pt:
                    if not active_id.is_discount:
                        active_id.show_discount_button = True
                else:
                    active_id.show_discount_button = False
        else:
            active_id.show_discount_button = False
