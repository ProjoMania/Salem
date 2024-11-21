from odoo import models, api, fields, _
from dateutil.relativedelta import relativedelta
import datetime


class BillingWiz(models.TransientModel):
    _name = 'purchase.billing.wiz'

    type = fields.Selection(string="Tracking Order Type", selection=[('new', 'Create New Tracking Order'),
                                                                     ('exist', 'Link with Existing Tracking Order')],
                            required=True, default="new")
    po_id = fields.Many2one("purchase.order")
    partner_id = fields.Many2one("res.partner")
    tracking_id = fields.Many2one("shipment.doc.tracking", 'Tracking Order')

    def action_apply(self):
        if self.type == 'new':
            doc_list = []
            for doc in self.partner_id.doc_type_ids:
                deadline = datetime.datetime.now()
                if doc.date_deadline_type == 'hours':
                    deadline += relativedelta(hours=doc.date_deadline)
                elif doc.date_deadline_type == 'days':
                    deadline += relativedelta(days=doc.date_deadline)
                doc_list.append((0, 0, {
                        'doc_type_id': doc.id,
                        'description': doc.description,
                        'assigned_to': doc.assigned_to.id or False,
                        'date_deadline': deadline
                    }))
            self.tracking_id = self.env['shipment.doc.tracking'].create({
                'partner_id': self.partner_id.id,
                'partner_ref': self.po_id.partner_ref,
                'doc_ids': doc_list
            })
            self.po_id.tracking_id = self.tracking_id.id
        else:
            self.po_id.tracking_id = self.tracking_id.id
        return self.po_id._action_create_invoice()
