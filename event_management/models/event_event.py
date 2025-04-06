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


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _get_default_stage_id(self):
        state_id = self.env.ref('event_management.event_stage_draft').id
        return self.env['event.stage'].search([('id', '=', state_id)], limit=1)

    def _get_default_pre_event_attachment(self):
        attachment_list_ids = []
        agenda_id = self.env.ref('event_management.event_attachment_name_agenda').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : agenda_id,
                'event_id' : self.id
            }))
        speaker_cv_id = self.env.ref('event_management.event_attachment_speaker_cv').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_cv_id,
                'event_id' : self.id
            }))
        speaker_contract_id = self.env.ref('event_management.event_attachment_speaker_contract').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_contract_id,
                'event_id' : self.id
            }))
        speaker_slide_kit_id = self.env.ref('event_management.event_attachment_slide_kit').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_slide_kit_id,
                'event_id' : self.id
            }))
        speaker_venue_id = self.env.ref('event_management.event_attachment_venue').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_venue_id,
                'event_id' : self.id
            }))
        speaker_opening_script_id = self.env.ref('event_management.event_attachment_opening_script').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_opening_script_id,
                'event_id' : self.id
            }))
        speaker_invitation_id = self.env.ref('event_management.event_attachment_invitation').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : speaker_invitation_id,
                'event_id' : self.id
            }))
        return attachment_list_ids

    def _get_default_budget_name(self):
        event_budget_ids = []
        budget_venue_id = self.env.ref('event_management.budget_name_venue_rental').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_venue_id,
                'event_id' : self.id
            }))
        budget_catering_id = self.env.ref('event_management.budget_name_catering_food').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_catering_id,
                'event_id' : self.id
            }))
        budget_marketing_id = self.env.ref('event_management.budget_name_market_advert').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_marketing_id,
                'event_id' : self.id
            }))
        budget_guest_id = self.env.ref('event_management.budget_name_speaker_guests').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_guest_id,
                'event_id' : self.id
            }))
        budget_logistics_id = self.env.ref('event_management.budget_name_logistics').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_logistics_id,
                'event_id' : self.id
            }))
        budget_decoration_id = self.env.ref('event_management.budget_name_decoration').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_decoration_id,
                'event_id' : self.id
            }))
        budget_entertainment_id = self.env.ref('event_management.budget_name_entertainment').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_entertainment_id,
                'event_id' : self.id
            }))
        budget_security_id = self.env.ref('event_management.budget_name_security').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_security_id,
                'event_id' : self.id
            }))

        budget_miscellaneous_id = self.env.ref('event_management.budget_name_miscellaneous').id
        event_budget_ids.append((0,0, {
                'budget_id' : budget_miscellaneous_id,
                'event_id' : self.id
            }))
        return event_budget_ids

    
    @api.depends('registration_ids.state', 'registration_ids.active')
    def calculate_actual_attendees(self):
        for record in self:
            registration_ids = self.env['event.registration'].search([('state', '=', 'done'),('event_id', '=', record.id)]).ids
            record.write({'actual_attendees_count': len(registration_ids)})

    @api.depends('estimated_cost', 'total_cost')
    def calculate_variance_amount(self):
        variance_amount = 0.00
        for record in self:
            variance_amount = record.estimated_cost - record.total_cost
            record.write({'variance': variance_amount})


    @api.depends('event_budget_ids','event_budget_ids.actual_cost')
    def calculate_actual_amount(self):
        amount = 0.00
        for record in self:
            for budget_line in record.event_budget_ids:
                amount += budget_line.actual_cost
            record.write({'total_cost': amount})

    @api.depends('event_budget_ids','event_budget_ids.estimated_cost')
    def calculate_estimated_amount(self):
        amount = 0.00
        for record in self:
            for budget_line in record.event_budget_ids:
                amount += budget_line.estimated_cost
            record.write({'estimated_cost': amount})

    @api.onchange('stage_id')
    def get_stage_name(self):
        draft_state_id = self.env.ref('event_management.event_stage_draft').name
        pre_pending_approval_id = self.env.ref('event_management.event_stage_pending_approval').name
        stage_scheduled_id = self.env.ref('event_management.event_stage_scheduled').name
        post_pending_approval_id = self.env.ref('event_management.event_stage_post_pending_approval').name
        completed_id = self.env.ref('event_management.event_stage_completed').name
        rejected_id = self.env.ref('event_management.event_stage_rejected').name
        if self.stage_id.name == draft_state_id:
            self.write({'state_name': draft_state_id})
        elif self.stage_id.name == pre_pending_approval_id:
            self.write({'state_name': pre_pending_approval_id})
        elif self.stage_id.name == stage_scheduled_id:
            self.write({'state_name': stage_scheduled_id})
        elif self.stage_id.name == post_pending_approval_id:
            self.write({'state_name': post_pending_approval_id})
        elif self.stage_id.name == completed_id:
            self.write({'state_name': completed_id})
        elif self.stage_id.name == rejected_id:
            self.write({'state_name': rejected_id})


    name = fields.Char(string='Event', translate=True, required=True, tracking=True)
    product_ids = fields.Many2many('product.template', string="Product", tracking=True, required=True)
    estimated_attendees = fields.Integer(string="Estimated Attendees", tracking=True, required=True)
    estimated_cost = fields.Float(string="Estimated Cost", tracking=True, required=True, compute='calculate_estimated_amount')
    honorarium_amount = fields.Float(string="Honorarium Amount", tracking=True, required=True)
    speaker = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', tracking=True, required=True)
    project_manager_id = fields.Many2one('hr.employee', string="Manager", tracking=True, required=True)
    speaker_specialty = fields.Text(string="Speaker Specialty", tracking=True, )
    event_type = fields.Selection([('rtd', 'RTD'), ('local', 'Local Speaker Event'), 
                                    ('sponsorship', 'Local Sponsorship'), ('ava', 'AVA'),
                                      ('regional', 'Regional Sponsorship'),('international', 'International Sponsorship'),
                                      ('external', 'External Standalone')], tracking=True, required=True)
    reason = fields.Text(string="Reason")
    actual_attendees_count = fields.Integer(string="Actual Attendees Count", tracking=True, compute='calculate_actual_attendees',
        readonly=True)
    total_cost = fields.Float(string="Total Cost", tracking=True, compute='calculate_actual_amount')
    variance = fields.Float(string="Variance", tracking=True, compute='calculate_variance_amount', readonly=True)
    attachment_ids = fields.One2many(
        'pre.event.attachment', 'event_id', string='Attachments', default=_get_default_pre_event_attachment)
    post_attachment_ids = fields.One2many(
        'post.event.attachment', 'post_event_id', string='Attachments')
    stage_id = fields.Many2one(
        'event.stage', ondelete='restrict', default=_get_default_stage_id,
        group_expand='_read_group_stage_ids', tracking=True, copy=False)
    state_name = fields.Char(string="State Name")
    event_budget_ids = fields.One2many(
        'event.budget', 'event_id', string='Budget Details', default=_get_default_budget_name, tracking=True)

    def event_submit_for_approval(self):
        state_id = self.env.ref('event_management.event_stage_pending_approval')
        #self.write({'state_name': state_id.name})
        if not self.estimated_cost:
            raise ValidationError(_('You must fill the estimated cost of event before submit for approval.'))
        if not self.honorarium_amount:
            raise ValidationError(_('You must fill the honorarium amount of event before submit for approval.'))
        if not self.estimated_attendees:
            raise ValidationError(_('You must fill the estimated attendees of event before submit for approval.'))
        for each_attachment in self.attachment_ids:
            if not each_attachment.ir_attachment_ids:
                raise ValidationError(_('You must upload the document for %s.'
                                        % (each_attachment.event_attachment_id.name)))
        for event_budget in self.event_budget_ids:
            if not event_budget.estimated_cost:
                raise ValidationError(_('You must fill the estimated cost in budget details %s.'
                                        % (event_budget.budget_id.name)))
        self.write({'stage_id': state_id.id, 'state_name': state_id.name})

    def pre_event_approved(self):
        state_id = self.env.ref('event_management.event_stage_scheduled')
        #self.write({'state_name': state_id.name})
        attachment_list_ids = []
        invoice_id = self.env.ref('event_management.event_attachment_invoice').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : invoice_id,
                'post_event_id' : self.id
            }))
        event_pic_id = self.env.ref('event_management.event_attachment_event_picture').id
        attachment_list_ids.append((0,0, {
                'event_attachment_id' : event_pic_id,
                'post_event_id' : self.id
            }))
        self.write({'stage_id': state_id.id, 'state_name': state_id.name,
                    'post_attachment_ids': attachment_list_ids})

    def pre_event_rejected(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Reason'),
            'res_model': 'reject.request.reason',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    def post_event_pending_approval(self):
        state_id = self.env.ref('event_management.event_stage_post_pending_approval')
        if not self.total_cost:
            raise ValidationError(_('You must fill the actual cost of event before submit the post event.'))
        for post_attachment in self.post_attachment_ids:
            if not post_attachment.ir_attachment_ids:
                raise ValidationError(_('You must upload the document for %s.'
                                        % (post_attachment.event_attachment_id.name)))
        for event_budget in self.event_budget_ids:
            if not event_budget.actual_cost:
                raise ValidationError(_('You must fill the actual cost in budget details %s.'
                                        % (event_budget.budget_id.name)))

        self.write({'stage_id': state_id.id, 'state_name': state_id.name})

    def event_completed(self):
        state_id = self.env.ref('event_management.event_stage_completed')
        self.write({'stage_id': state_id, 'state_name': state_id.name})


class EventAttachment(models.Model):
    _name = 'event.attachment'

    name = fields.Char('Name', required=True)


class PreEventAttachment(models.Model):
    _name = 'pre.event.attachment'

    event_attachment_id = fields.Many2one('event.attachment', string="Name",required=True)
    ir_attachment_ids = fields.Many2many('ir.attachment', string="File")
    event_id = fields.Many2one('event.event', string="Event")


class PostEventAttachment(models.Model):
    _name = 'post.event.attachment'

    event_attachment_id = fields.Many2one('event.attachment', string="Name",required=True)
    ir_attachment_ids = fields.Many2many('ir.attachment', string="File")
    post_event_id = fields.Many2one('event.event', string="Event")


class reject_request_reason(models.TransientModel):
    _name = 'reject.request.reason'

    name = fields.Text(string="Reason", required=True)

    def add_reason(self):
        event_id = self.env['event.event'].search([('id', '=', self._context.get('active_id'))])
        state_id = self.env.ref('event_management.event_stage_rejected')
        event_id.write({'reason': self.name, 'stage_id': state_id, 'state_name': state_id.name})
