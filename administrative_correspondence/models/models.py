# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from random import randint


class AdministrativeCorrespondenceTags(models.Model):
    _name = 'administrative.correspondence.tags'
    _rec_name = 'name'
    _description = 'Administrative Correspondence Tags'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Tag Name", required=True, )
    color = fields.Integer(string="Color", required=False, default=_get_default_color)


class AdministrativeCorrespondenceAttachments(models.Model):
    _name = 'administrative.correspondence.attachment'
    _rec_name = 'name'
    _description = 'Administrative Correspondence Attachments'

    name = fields.Char(string="Description", required=True, )
    file = fields.Binary('Attachment', attachment=True)
    file_name = fields.Char('File Name')
    correspondence_id = fields.Many2one(comodel_name="administrative.correspondence", string="Correspondence", required=True, )

    def download_file(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/administrative.correspondence.attachment/%s/file/%s?download=true' % (self.id, self.file_name),
            'target': 'self',
        }


class AdministrativeCorrespondenceTemplate(models.Model):
    _name = 'administrative.correspondence.template'
    _rec_name = 'name'
    _description = 'Administrative Correspondence Template'

    name = fields.Char(string="Name", required=True, )
    body = fields.Html(string="Body", )


class AdministrativeCorrespondence(models.Model):
    _name = 'administrative.correspondence'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Administrative Correspondence'

    name = fields.Char(string="Sequence No.", required=True, default=_("New"))
    active = fields.Boolean(string="Active", default=True)
    validated_by_id = fields.Many2one(comodel_name="res.users", string="Validated by", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="Issued By", required=True, default=lambda self: self.env.user)
    assigned_id = fields.Many2one(comodel_name="res.users", string="Assigned To", required=True, default=lambda self: self.env.user)
    template_id = fields.Many2one(comodel_name="administrative.correspondence.template", string="Subject", required=True, )
    type = fields.Selection(string="Type", selection=[('internal', 'Internal'), ('inbound', 'Inbound'), ('outbound', 'Outbound')], required=True, )
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=False, default=lambda self: self.env.company)
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('submitted', 'Submitted'), ('pending', 'Pending'), ('cancelled', 'Cancelled') ], required=True, default='draft')
    created_on = fields.Date(string="Created On", required=True, default=fields.Date.context_today)
    sent_from_id = fields.Many2one(comodel_name="res.partner", string="Correspondence From", required=False, )
    sent_to_id = fields.Many2one(comodel_name="res.partner", string="Correspondence To", required=False, )
    parent_id = fields.Many2one(comodel_name="administrative.correspondence", string="Parent Correspondence", required=False, )
    correspondence_attachment_ids = fields.One2many(comodel_name="administrative.correspondence.attachment", inverse_name="correspondence_id", string="Attachments", required=False, )
    tag_ids = fields.Many2many(comodel_name="administrative.correspondence.tags", relation="administrative_correspondence_tags_rel", column1="correspondence_id", column2="tag_id", string="Tags", )
    body = fields.Html(string="Correspondence Body", )

    @api.onchange('template_id')
    def _onchange_template_id(self):
        self.body = self.template_id.body

    def set_pending(self):
        self.state = 'pending'

    def set_submitted(self):
        self.state = 'submitted'
        self.validated_by_id = self.env.user.id

    def set_cancelled(self):
        self.state = 'cancelled'

    def reset_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, values):
        if values.get('company_id'):
            correspondence_type = values.get('type') or self._context.get('type')
            sequence_code = 'administrative.correspondence.%s' % correspondence_type
            sequence = self.env['ir.sequence'].search([('company_id', '=', values.get('company_id')), ('code', '=', sequence_code)])
            values.update({'name': sequence.next_by_id()})
        return super(AdministrativeCorrespondence, self).create(values)


class Company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    @api.model
    def create(self, vals):
        company = super(Company, self).create(vals)
        company.sudo()._create_per_company_correspondence_sequences()
        return company

    @api.model
    def create_missing_inbound_correspondence_sequence(self):
        """
        This method will be called once when install the module to create the inbound sequences for all existing companies
        :return:
        """
        company_ids = self.env['res.company'].search([])
        company_has_correspondence_seq = self.env['ir.sequence'].search([('code', '=', 'administrative.correspondence.inbound')]).mapped('company_id')
        company_todo_sequence = company_ids - company_has_correspondence_seq
        company_todo_sequence._create_inbound_correspondence_sequence()

    @api.model
    def create_missing_outbound_correspondence_sequence(self):
        """
        This method will be called once when install the module to create the outbound sequences for all existing companies
        :return:
        """
        company_ids = self.env['res.company'].search([])
        company_has_correspondence_seq = self.env['ir.sequence'].search(
            [('code', '=', 'administrative.correspondence.outbound')]).mapped('company_id')
        company_todo_sequence = company_ids - company_has_correspondence_seq
        company_todo_sequence._create_outbound_correspondence_sequence()

    @api.model
    def create_missing_internal_correspondence_sequence(self):
        """
        This method will be called once when install the module to create the internal sequences for all existing companies
        :return:
        """
        company_ids = self.env['res.company'].search([])
        company_has_correspondence_seq = self.env['ir.sequence'].search(
            [('code', '=', 'administrative.correspondence.internal')]).mapped('company_id')
        company_todo_sequence = company_ids - company_has_correspondence_seq
        company_todo_sequence._create_internal_correspondence_sequence()

    def _create_per_company_correspondence_sequences(self):
        self.ensure_one()
        self._create_inbound_correspondence_sequence()
        self._create_internal_correspondence_sequence()
        self._create_outbound_correspondence_sequence()

    def _create_inbound_correspondence_sequence(self):
        inbound_vals = []
        for company in self:
            inbound_vals.append({
                'name': '%s Admin. Corres. Inbound Sequence' % company.name,
                'code': 'administrative.correspondence.inbound',
                'company_id': company.id,
                'prefix': 'BDI-IN-%(year)s-',
                'padding': 4,
                'number_next': 1,
                'number_increment': 1
            })
        if inbound_vals:
            self.env['ir.sequence'].create(inbound_vals)

    def _create_outbound_correspondence_sequence(self):
        outbound_vals = []
        for company in self:
            outbound_vals.append({
                'name': '%s Admin. Corres. Outbound Sequence' % company.name,
                'code': 'administrative.correspondence.outbound',
                'company_id': company.id,
                'prefix': 'BDI-OUT-%(year)s-',
                'padding': 4,
                'number_next': 1,
                'number_increment': 1
            })
        if outbound_vals:
            self.env['ir.sequence'].create(outbound_vals)

    def _create_internal_correspondence_sequence(self):
        internal_vals = []
        for company in self:
            internal_vals.append({
                'name': '%s Admin. Corres. Internal Sequence' % company.name,
                'code': 'administrative.correspondence.internal',
                'company_id': company.id,
                'prefix': 'BDI-INT-%(year)s-',
                'padding': 4,
                'number_next': 1,
                'number_increment': 1
            })
        if internal_vals:
            self.env['ir.sequence'].create(internal_vals)


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'
    
    category = fields.Selection(selection_add=[('administrative_correspondence', 'Administrative Correspondence')])
