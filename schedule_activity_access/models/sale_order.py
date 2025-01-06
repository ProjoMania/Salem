# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    # Inherited to add 'Rejected by Customer' in state field
    _inherit = 'sale.order'

    # state = fields.Selection(selection_add=[
    #     ('reject_by_customer', 'Rejected by Customer')])
    #
    # def action_rejected(self):
    #     # Method to change the state when 'REJECT BY CUSTOMER' button is
    #     # clicked
    #     self.ensure_one()
    #     self.write({'state': 'reject_by_customer'})
    #
    # def action_draft(self):
    #     # Overide to show the draft button in 'Rejected by Customer' state
    #     orders = self.filtered(lambda s: s.state in ['cancel', 'sent',
    #                                                  'reject_by_customer'])
    #     return orders.write({
    #         'state': 'draft',
    #         'signature': False,
    #         'signed_by': False,
    #         'signed_on': False,
    #     })

class MailActivity(models.Model):

    _inherit = 'mail.activity'

    @api.depends('res_model', 'res_id', 'user_id')
    def _compute_can_write(self):
        super(MailActivity, self)._compute_can_write()
        # valid_records = self._filter_access_rules('write')
        # print ("FFFFFFFFFFFFFFFFFFFFFF <<<<<<<<<,",valid_records)
        for record in self:
            record.can_write = False
            if self.env.user.has_group('schedule_activity_access.group_activity_administration') or self.env.user.id == record.user_id.id:
                record.can_write = True
