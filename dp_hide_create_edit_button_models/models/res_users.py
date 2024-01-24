# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools,_

class ResUser(models.Model):
    _inherit = 'res.users'

    hide_create_model_ids = fields.Many2many('ir.model','create_button_ir_model',string="Hide Create Button")
    hide_edit_model_ids = fields.Many2many('ir.model', 'edir_button_ir_model',string="Hide Edit Button")
