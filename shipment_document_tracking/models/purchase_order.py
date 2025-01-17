from odoo import fields, models, api, _
from odoo.tools import groupby
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tracking_id = fields.Many2one('shipment.doc.tracking', 'Tracking Order', copy=False)
    airways_ref = fields.Char('AIRWAYS BILL', copy=False)
    shipment_doc_count = fields.Integer(compute="_compute_shipment_doc_count", string='Shipment Doc Count', copy=False, default=0, store=True)
    
    @api.depends('tracking_id')
    def _compute_shipment_doc_count(self):
        env_shipment_doc_tracking = self.env['shipment.doc.tracking']
        for po in self:
            po.shipment_doc_count = env_shipment_doc_tracking.search_count([('po_id', '=', po.id)])

    def view_shipment_tracking(self):
        shipment_doc_tracking = self.env['shipment.doc.tracking'].search([('po_id', '=', self.id)])
        if len(shipment_doc_tracking) > 1:
            return {
                'name': _('Tracking Order'),
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': self.tracking_id._name,
                'domain': [('id', 'in', shipment_doc_tracking.ids)]
            }
        return {
            'name': _('Tracking Order'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form,list',
            'res_id': self.tracking_id.id,
            'res_model': self.tracking_id._name
        }


    def action_create_invoice(self):
        if self.env.company.allow_shipment_tracking:
            return {
                'name': _('Tracking Order'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'purchase.billing.wiz',
                'context': {'default_po_id': self.id, 'default_partner_id': self.partner_id.id}
            }
        else:
            return self._action_create_invoice()

    def _action_create_invoice(self):
        """Create the invoice associated to the PO.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        sequence = 10
        for order in self:
            if order.invoice_status != 'to invoice':
                continue

            order = order.with_company(order.company_id)
            pending_section = None
            # Invoice values.
            invoice_vals = order._prepare_invoice()
            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if not float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    if pending_section:
                        line_vals = pending_section._prepare_account_move_line()
                        line_vals.update({'sequence': sequence})
                        invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                        sequence += 1
                        pending_section = None
                    line_vals = line._prepare_account_move_line()
                    line_vals.update({'sequence': sequence})
                    invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                    sequence += 1
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise UserError(_('There is no invoiceable line. If a product has a control policy based on received quantity, please make sure that a quantity has been received.'))

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (x.get('company_id'), x.get('partner_id'), x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= AccountMove.with_company(vals['company_id']).create(vals)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        moves.filtered(lambda m: m.currency_id.round(m.amount_total) < 0).action_switch_move_type()
        return self.action_view_invoice(moves)

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')

        partner_invoice = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice'])
        partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]

        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'partner_id': partner_invoice.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(partner_invoice)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': partner_bank_id.id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'tracking_id': self.tracking_id.id or False,
        }
        return invoice_vals

    def action_create_sdt_manually(self, creation_type=None):
            doc_list = []
            if self.invoice_count == 1 or creation_type == 'consolidated':
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
                    'partner_ref': self.partner_ref,
                    'airways_ref': self.airways_ref,
                    'doc_ids': doc_list
                })
            else:
                action = self.env.ref('shipment_document_tracking.action_create_sdt_manually').read()[0]
                return action
