# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import calendar
from datetime import datetime
from pytz import timezone, utc
from dateutil.relativedelta import relativedelta

month_selection = [
    ('1', '01'), ('2', '02'), ('3', '03'),
    ('4', '04'), ('5', '05'), ('6', '06'),
    ('7', '07'), ('8', '08'), ('9', '09'),
    ('10', '10'), ('11', '11'), ('12', '12')
]


class ProductionLot(models.Model):
    _inherit = 'stock.lot'
    _order = 'life_date asc, state asc, id asc'

    def _get_total_duration(self):
        for lot in self:
            end_date = datetime.now()
            if lot.approved_date:
                end_date = lot.approved_date
            # print('diff.total_seconds().....', diff.total_seconds())
            lot.update({
                'total_duration': (end_date - lot.create_date).days,
                'last_update_duration': (datetime.now() - lot.last_update_date).days,
            })

    @api.depends('attach_request_document')
    def _attachment_request_document(self):
        for data in self:
            val = data.request_attachment_id.datas
            data.attach_request_document = val

    def _set_request_document_filename(self):
        Attachment = self.env['ir.attachment']
        # if self.attach_request_document_filename and not self.attach_request_document_filename.endswith('.pdf'):
        #     raise UserError(_('Design attachment file extension should be .pdf !'))
        if self.attach_request_document:
            attachment_value = {
                'name': self.attach_request_document_filename or '',
                'datas': self.attach_request_document or '',
                'store_fname': self.attach_request_document_filename or '',
                'type': 'binary',
                'res_model': "stock.lot",
                'res_id': self.id,
            }
            attachment = Attachment.sudo().create(attachment_value)
            self.request_attachment_id = attachment.id
        else:
            self.request_attachment_id = False





    @api.depends('attach_approval_document')
    def _attachment_approval_document(self):
        for data in self:
            val = data.approval_attachment_id.datas
            data.attach_approval_document = val

    def _set_approval_document_filename(self):
        Attachment = self.env['ir.attachment']
        # if self.attach_approval_document_filename and not self.attach_approval_document_filename.endswith('.pdf'):
        #     raise UserError(_('Design attachment file extension should be .pdf !'))
        if self.attach_approval_document:
            attachment_value = {
                'name': self.attach_approval_document_filename or '',
                'datas': self.attach_approval_document or '',
                'store_fname': self.attach_approval_document_filename or '',
                'type': 'binary',
                'res_model': "stock.lot",
                'res_id': self.id,
            }
            attachment = Attachment.sudo().create(attachment_value)
            self.approval_attachment_id = attachment.id
        else:
            self.approval_attachment_id = False


     

#added by abdulrahman

    @api.depends('attach_meda_document')
    def _attachment_meda_document(self):
        for data in self:
            val = data.meda_attachment_id.datas
            data.attach_meda_document = val


    def _set_meda_document_filename(self):
        Attachment = self.env['ir.attachment']
        # if self.attach_approval_document_filename and not self.attach_approval_document_filename.endswith('.pdf'):
        #     raise UserError(_('Design attachment file extension should be .pdf !'))
        if self.attach_meda_document:
            attachment_value = {
                'name': self.attach_meda_document_filename or '',
                'datas': self.attach_meda_document or '',
                'store_fname': self.attach_meda_document_filename or '',
                'type': 'binary',
                'res_model': "stock.lot",
                'res_id': self.id,
            }
            attachment = Attachment.sudo().create(attachment_value)
            self.meda_attachment_id = attachment.id
        else:
            self.meda_attachment_id = False

# end lines added by abdulrahman  




    @api.depends('alert_date')
    def _compute_product_expiry_alert(self):
        current_date = fields.Datetime.now().date()
        lots = self.filtered(lambda l: l.alert_date)
        for lot in lots:
            lot.product_expiry_alert = lot.alert_date <= current_date
        (self - lots).product_expiry_alert = False

    @api.depends('life_date', 'use_date')
    def _compute_date_format(self):
        for lot in self:
            life_date_format, use_date_format = False, False
            if lot.life_date:
                life_date_format = lot.life_date.strftime('%m/%Y')
            if lot.use_date:
                use_date_format = lot.use_date.strftime('%m/%Y')
            lot.life_date_format = life_date_format
            lot.update({
                'life_date_format': life_date_format,
                'use_date_format': use_date_format,
            })

    @api.depends('create_date')
    def _compute_date_created(self):
        tzinfo = 'Asia/Baghdad'
        for lot in self:
            create_date = lot.create_date or datetime.now()
            lot.date_created = timezone(tzinfo).localize(create_date).astimezone(utc).date()

    attach_request_document = fields.Binary('QC Release Doc', compute='_attachment_request_document',
                                            inverse='_set_request_document_filename', copy=False)
    attach_request_document_filename = fields.Char('Request Filename', copy=False)
    request_attachment_id = fields.Many2one('ir.attachment', 'Request Attachment', copy=False)

    attach_approval_document = fields.Binary('Sticker Release Doc', compute='_attachment_approval_document',
                                             inverse='_set_approval_document_filename', copy=False)
    attach_approval_document_filename = fields.Char('Approval Filename', copy=False)
    approval_attachment_id = fields.Many2one('ir.attachment', 'Approval Attachment', copy=False)

#added by abdulrahman
    attach_meda_document = fields.Binary('Manufacturer Release Doc', compute='_attachment_meda_document',
                                             inverse='_set_meda_document_filename', copy=False)
    attach_meda_document_filename = fields.Char('meda Filename', copy=False)
    meda_attachment_id = fields.Many2one('ir.attachment', 'meda Attachment', copy=False) 

# end lines added by abdulrahman  

    state = fields.Selection([('progress', 'Quarantine'), ('approved', 'Released'),
                              ('rejected', 'Rejected')], default='progress', string='Status', tracking=True)
    approved_date = fields.Datetime('Released Date', tracking=True)
    last_update_date = fields.Datetime('Last Update Date', tracking=True, default=fields.Datetime.now)
    total_duration = fields.Integer('Total Duration(Days) ', compute='_get_total_duration')
    last_update_duration = fields.Integer('Last Update Duration(Days)', compute='_get_total_duration')
    life_date = fields.Date(string='End of Life Date',
                            help='This is the date on which the goods with this Serial Number may become dangerous and must not be consumed.')
    use_date = fields.Date(string='Best before Date',
                           help='This is the date on which the goods with this Serial Number start deteriorating, without being dangerous yet.')
    removal_date = fields.Date(string='Removal Date',
                               help='This is the date on which the goods with this Serial Number should be removed from the stock. This date will be used in FEFO removal strategy.')
    alert_date = fields.Date(string='Alert Date',
                             help='Date to determine the expired lots and serial numbers using the filter "Expiration Alerts".')
    product_expiry_alert = fields.Boolean(compute='_compute_product_expiry_alert',
                                          help="The Alert Date has been reached.")
    life_date_format = fields.Char('End of Life Date', compute='_compute_date_format',
                                   help="Function to compute Month/Year Date format.")
    use_date_format = fields.Char('Best before Date', compute='_compute_date_format',
                                   help="Function to compute Month/Year Date format.")
    life_date_month = fields.Selection(month_selection, string='End of Life Month', copy=False,
                                       help='This is the date on which the goods with this Serial Number may become dangerous and must not be consumed.')
    life_date_year = fields.Selection([(str(num), str(num)) for num in range(
        ((datetime.now().year)), ((datetime.now().year) + 100))], string='End of Life Year', copy=False)
    use_date_month = fields.Selection(month_selection, string='Best before Month', copy=False,
                                      help='This is the date on which the goods with this Serial Number start deteriorating, without being dangerous yet.')
    use_date_year = fields.Selection([(str(num), str(num)) for num in range(
        ((datetime.now().year)), ((datetime.now().year) + 100))], string='Best before Year', copy=False)
    removal_date_month = fields.Selection(month_selection, string='Removal Month', copy=False,
                                          help='This is the date on which the goods with this Serial Number should be removed from the stock. This date will be used in FEFO removal strategy.')
    removal_date_year = fields.Selection([(str(num), str(num)) for num in range(
        ((datetime.now().year)), ((datetime.now().year) + 100))], string='Removal Year', copy=False)
    alert_date_month = fields.Selection(month_selection, string='Alert Month', copy=False,
                                        help='Date to determine the expired lots and serial numbers using the filter "Expiration Alerts".')
    alert_date_year = fields.Selection([(str(num), str(num)) for num in range(
        ((datetime.now().year)), ((datetime.now().year) + 100))], string='Alert Year', copy=False)
    date_created = fields.Date('Date Created', compute='_compute_date_created', index=True, readonly=True, store=True)
    numbering_label = fields.Char('Numbering Label')

    _sql_constraints = [
        ('name_ref_uniq', 'unique (name, product_id, company_id, create_date)',
         'The combination of serial number and product must be unique across a company and created date !'),
    ]

    # @api.constrains('name', 'product_id', 'company_id')
    # def _check_name_ref_uniq(self):
    #     for record in self:
    #         other_lots = self.search([('name', '=', record.name), ('product_id', '!=', record.product_id.id)])
    #         if len(other_lots) > 0:
    #             raise ValidationError(_('Lot Number "%s" is used by another product "%s"' %
    #                                     (record.name, other_lots[0].product_id.name)))

    # @api.onchange('life_date_year')
    # def _onchange_year(self):
    #     if self.life_date_year and int(self.life_date_year) < datetime.now().year:
    #         raise ValidationError(_("Can not be past date ..!"))

    @api.onchange('life_date_month', 'life_date_year')
    def _onchange_life_month(self):
        if self.life_date_month and self.life_date_year:
            try:
                res = datetime.strptime(str(1) + str(self.life_date_month) + str(self.life_date_year), '%d%m%Y')
            except Exception as e:
                print("error", e)
                raise ValidationError(_('Invalid Date'))
            range = calendar.monthrange(int(self.life_date_year), int(self.life_date_month))
            self.life_date = str(self.life_date_year) + '-' + str(self.life_date_month) + '-' + str(range[1])

    @api.onchange('use_date_month', 'use_date_year')
    def _onchange_use_month(self):
        if self.use_date_month and self.use_date_year:
            try:
                res = datetime.strptime(str(1) + str(self.use_date_month) + str(self.use_date_year), '%d%m%Y')
            except Exception as e:
                print("error", e)
                raise ValidationError(_('Invalid Date'))
            range = calendar.monthrange(int(self.use_date_year), int(self.use_date_month))
            self.use_date = str(self.use_date_year) + '-' + str(self.use_date_month) + '-' + str(range[1])

    @api.onchange('removal_date_month', 'removal_date_year')
    def _onchange_removal_month(self):
        if self.removal_date_month and self.removal_date_year:
            try:
                res = datetime.strptime(str(1) + str(self.removal_date_month) + str(self.removal_date_year), '%d%m%Y')
            except Exception as e:
                print("error", e)
                raise ValidationError(_('Invalid Date'))
            range = calendar.monthrange(int(self.removal_date_year), int(self.removal_date_month))
            self.removal_date = str(self.removal_date_year) + '-' + str(self.removal_date_month) + '-' + str(range[1])

    @api.onchange('alert_date_month', 'alert_date_year')
    def _onchange_alert_month(self):
        if self.alert_date_month and self.alert_date_year:
            try:
                res = datetime.strptime(str(1) + str(self.alert_date_month) + str(self.alert_date_year), '%d%m%Y')
            except Exception as e:
                print("error", e)
                raise ValidationError(_('Invalid Date'))
            range = calendar.monthrange(int(self.alert_date_year), int(self.alert_date_month))
            self.alert_date = str(self.alert_date_year) + '-' + str(self.alert_date_month) + '-' + str(range[1])

    @api.model
    def create(self, vals):
        vals['state'] = 'progress'
        return super(ProductionLot, self).create(vals)

    def in_progress(self):
        if not self.request_attachment_id:
            raise UserError(_('Please upload request document first !'))
        self.state = 'progress'
        self.last_update_date = datetime.now()

    def approve(self):
        if not self.approval_attachment_id:
            raise UserError(_('Please upload approval document first !'))
        self.state = 'approved'
        self.approved_date = datetime.now()
        self.last_update_date = datetime.now()

    def reject(self):
        self.state = 'rejected'
        self.last_update_date = datetime.now()

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        context = self._context or {}
        if context.get('only_approved', False):
            domain += [('state', '=', 'approved')]
        return super(ProductionLot, self)._search(domain, offset, limit, order,
                                               access_rights_uid=access_rights_uid)
