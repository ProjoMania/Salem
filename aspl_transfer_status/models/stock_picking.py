# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    attachment_ids = fields.One2many('stock.picking.attachment', 'picking_id', string='Attachments')
    transfer_status_id = fields.Many2one('transfer.status', string="Transfer Status")
    required_attachment = fields.Integer(related='transfer_status_id.attachment_file', string='Required Attachment')
    is_close = fields.Boolean(string='Is Close', )

    def write(self, vals):
        if 'transfer_status_id' in vals:
            transfer_status_id = self.env['transfer.status'].search([('id', '=', vals.get('transfer_status_id'))])
            if transfer_status_id:
                vals.update({'is_close': transfer_status_id.status_id.is_close})
        return super().write(vals)


    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        if self.picking_type_id:
            status_ids = self.env['transfer.status'].search([('picking_type_ids', 'in', self.picking_type_id.id)])
            self.transfer_status_id = False
            self.attachment_ids = [(5, 0, 0)]
            return {'domain': {'transfer_status_id': [('id', 'in', status_ids.ids)]}}

    @api.onchange('transfer_status_id')
    def onchange_transfer_status_id(self):
        if self.transfer_status_id:
            attachment_number = self.transfer_status_id.attachment_file
            # self.required_attachment = attachment_number
            if attachment_number != len(self.attachment_ids) and self.transfer_status_id.status_id.is_close:
                raise ValidationError('Please upload %s attachments in Attachments Tab.' %attachment_number)


    # @api.model
    # def create(self, vals):
    #     res = super().create(vals)
    #     transfer_status_id = self.env['transfer.status'].search([('id', '=', vals.get('transfer_status_id'))])
    #     if transfer_status_id:
    #         attachment_number = transfer_status_id.attachment_file
    #         if attachment_number != len(vals.get('attachment_ids')):
    #             raise ValidationError('Please upload %s attachments in Attachments Tab.' % attachment_number)
    #     return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
