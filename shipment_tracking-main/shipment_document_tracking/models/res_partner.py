# -*- coding: utf-8 -*-

from odoo import fields, models, _


class DocType(models.Model):
    _name = 'doc.type'
    _description = 'doc type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')
    partner_id = fields.Many2one('res.partner', string="Partner")
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    date_deadline_type = fields.Selection(string="Deadline Type", selection=[('hours', 'Hours'), ('days', 'Days')],
                                          required=True, default='days')
    date_deadline = fields.Float(string="Deadline Amount", default=5)


class Partner(models.Model):
    _inherit = ['res.partner']

    doc_type_ids = fields.One2many('doc.type', 'partner_id', string="Documents")
