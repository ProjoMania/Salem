# -*- coding: utf-8 -*-

from odoo import fields, models
import datetime
from dateutil.relativedelta import relativedelta


class CreateSdtManually(models.TransientModel):
    _name = 'create.sdt.manually'
    _description = 'Create Shipment Document Tracking Manually'
    _rec_name = 'po_id'

    po_id = fields.Many2one('purchase.order', 'Purchase Order', required=True)
    creation_type = fields.Selection([('splitted', 'Splitted'), ('consolidated', 'Consolidated')], 'Creation Type',
                                     required=True, default="splitted")

    def action_apply(self):
        if self.creation_type == 'consolidated':
            self.po_id.action_create_sdt_manually(creation_type='consolidated')
        else:
            partner = self.po_id.partner_id
            env_shipment_doc_tracking = self.env['shipment.doc.tracking']
            for invoice in self.po_id.invoice_ids:
                doc_list = []
                for doc in partner.doc_type_ids:
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
                self.po_id.tracking_id = env_shipment_doc_tracking.create({
                    'partner_id': partner.id,
                    'partner_ref': self.po_id.partner_ref,
                    'airways_ref': self.po_id.airways_ref,
                    'po_id': self.po_id.id,
                    'bill_ids': [(6, 0, [invoice.id])],
                    'doc_ids': doc_list
                })