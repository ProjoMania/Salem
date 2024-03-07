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


class TransferStatus(models.Model):
    _name = 'transfer.status'
    _description = 'Transfer Status'


    name = fields.Char(string='Name', required=True)
    attachment_file = fields.Integer(string='Attachment File')
    picking_type_ids = fields.Many2many('stock.picking.type', string="Picking Type", required=True)
    status_id = fields.Many2one('transfer.status.state', string="Status", required=True)


class TransferStatusState(models.Model):
    _name = 'transfer.status.state'
    _description = 'Transfer Status State'

    name = fields.Char(string='Name')
    is_close = fields.Boolean(string='Is Close')



class StockPickingAttachment(models.Model):
    _name = 'stock.picking.attachment'
    _description = 'Stock Picking Attachment'

    name = fields.Char(string='Name')
    date = fields.Datetime(string='Date', readonly=True, default=lambda self: fields.Datetime.now())
    file_url = fields.Char(string='File URL')
    file = fields.Binary(string='File')
    picking_id = fields.Many2one('stock.picking', string='Picking')

    @api.constrains('file', 'file_url')
    def constrains_on_field(self):
        for record in self:
            if not record.file and not record.file_url:
                raise ValidationError("File Url or File should not be blank.")

    def download_attachment(self):
        return {
            "type": "ir.actions.act_url",
            'url': '/web/content/?model=stock.picking.attachment&id={}&field=file&filename_field=name&download=true'.format(
                self.id
            ),
            "target": "new"}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
