# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DocDoc(models.Model):
    _name = 'doc.doc'
    _rec_name = 'doc_type_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'doc doc'

    doc_type_id = fields.Many2one('doc.type', string='Name', required=True)
    description = fields.Text(string='Description')
    document_file = fields.Binary(string="Document", attachment=True)
    file_name = fields.Char(string='File Name')
    url=fields.Char(string="URL")
    tracking_id = fields.Many2one('shipment.doc.tracking')
    is_file_document = fields.Boolean(string="File")
    is_url_document = fields.Boolean(string="URL")
    uploaded_by = fields.Many2one('res.users', string="Uploaded By")
    uploaded_date = fields.Datetime(string="Uploaded Date")
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    validated_by = fields.Many2one('res.users', string="Validated By")
    date_done = fields.Datetime(string="Done Date")
    date_deadline = fields.Datetime(string="Deadline Date")
    is_uploaded = fields.Boolean(string="Is Uploaded", default=False ,compute="_compute_is_uploaded", store=True)
    is_reviewed = fields.Boolean(string="Is Reviewed", default=False)


    @api.depends('document_file','url')
    def _compute_is_uploaded(self):
        for record in self:
            if record.document_file or record.url:
                record.is_uploaded = True
                record.uploaded_date = fields.Datetime.now()
                record.uploaded_by = self.env.user.id
            else:
                record.is_uploaded = False

    def action_reviewed(self):
        self.is_reviewed = True
        self.validated_by = self.env.user.id
        self.date_done = fields.Datetime.now()