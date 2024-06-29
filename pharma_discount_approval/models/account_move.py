
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_discount = fields.Boolean(string='Discount')

    def action_post(self):
        res = super().action_post()
        if not self.env.user.has_group('base.group_erp_manager'):
            if self.is_discount:
                return res
            else:
                move = self.invoice_line_ids.filtered(lambda l: l.product_id.name == 'Discount')
                moves = self.invoice_line_ids.filtered(lambda l: l.discount > 0.0)
                if move:
                    if abs(move.price_unit) >= self.sales_rep_id.max_disc:
                        self.is_discount = False
                        raise UserError('You have exceeded the maximum limit of discount. '
                                        'Please ask other Sales Representative or Manager to approve.')
                if moves:
                    for each in moves:
                        discount_value = each.price_unit * each.discount / 100
                        if discount_value >= self.sales_rep_id.max_disc:
                            self.is_discount = False
                            raise UserError('You have exceeded the maximum limit of discount. '
                                            'Please ask other Sales Representative or Manager to approve.')
        return res

    def action_approve_invoice_discount(self):
        if not self.env.user.has_group('base.group_erp_manager'):
            if self.env.user == self.sales_rep_id:
                raise UserError('You are not allowed to approve the discount.')
            else:
                self.is_discount = True

    def action_open_invoice_discount_wizard(self):
        self.ensure_one()
        return {
            'name': _("Discount"),
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.discount',
            'view_mode': 'form',
            'target': 'new',
        }
