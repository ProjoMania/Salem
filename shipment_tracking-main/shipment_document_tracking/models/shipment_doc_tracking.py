# -*- coding: utf-8 -*-
# Part of Odoo.addons.shipment_document_tracking. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ShipmentDocTracking(models.Model):
    _name = 'shipment.doc.tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'shipment doc tracking'
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    status = fields.Selection(
        [('not_completed', 'Not Completed'), ('partial', 'Partially Completed'), ('complete', 'Completed')],
        string='Status', required=True, default="not_completed", compute="onchange_doc_ids")
    done_date = fields.Datetime(string="Done Date")
    partner_id = fields.Many2one('res.partner', string="Vendor")
    partner_ref = fields.Char('Vendor Reference', copy=False,
                              help="Reference of the sales order or bid sent by the vendor. "
                                   "It's used to do the matching when you receive the "
                                   "products as this reference is usually written on the "
                                   "delivery order sent by your vendor.")
    deadline = fields.Datetime(string="Deadline")
    doc_ids = fields.One2many('doc.doc', string="Documents", inverse_name="tracking_id")
    bill_ids = fields.One2many('account.move', string="Bills", inverse_name='tracking_id')
    po_ids = fields.One2many('purchase.order', string="Orders", inverse_name='tracking_id')
    purchase_order_count = fields.Integer(compute="_compute_origin_po_count", string='Purchase Order Count')
    invoice_count = fields.Integer(compute="_compute_invoice", string='Bill Count', copy=False, default=0, store=True)

    @api.depends('bill_ids')
    def _compute_invoice(self):
        for order in self:
            order.invoice_count = len(order.bill_ids)

    def action_view_invoice(self, invoices=False):
        """This function returns an action that display existing vendor bills of
        given purchase order ids. When only one found, show the vendor bill
        immediately.
        """
        if not invoices:
            self.invalidate_model(['bill_ids'])
            invoices = self.bill_ids

        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        # choose the view_mode accordingly
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result

    @api.depends('po_ids')
    def _compute_origin_po_count(self):
        for tracking in self:
            tracking.purchase_order_count = len(tracking.po_ids)

    def action_view_source_purchase_orders(self):
        self.ensure_one()
        result = self.env['ir.actions.act_window']._for_xml_id('purchase.purchase_form_action')
        if len(self.po_ids) > 1:
            result['domain'] = [('id', 'in', self.po_ids.ids)]
        elif len(self.po_ids) == 1:
            result['views'] = [(self.env.ref('purchase.purchase_order_form', False).id, 'form')]
            result['res_id'] = self.po_ids.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('shipment.doc.tracking')
        return super(ShipmentDocTracking, self).create(vals)

    @api.depends("doc_ids", "doc_ids.is_reviewed")
    def onchange_doc_ids(self):
        for rec in self:
            rec.status = 'not_completed'
            if rec.doc_ids:
                if all(doc.is_reviewed for doc in rec.doc_ids):
                    rec.status = 'complete'
                    rec.done_date = fields.Datetime.now()
                elif any(doc.is_reviewed for doc in rec.doc_ids):
                    rec.status = 'partial'
