# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
from . import models
from odoo.models import BaseModel
from lxml import etree

# fields_view_get_super = BaseModel.fields_view_get
#
# def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#     result = fields_view_get_super(self,view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
#
#     # by pass for root user
#     if self.env.uid == 1:
#         return result
#     app_check = self.env['ir.module.module'].search([('name','=','dp_hide_create_edit_button_models')], limit=1)
#     if app_check:
#         if app_check.state != 'installed':
#             return result
#
#     # hide create button on all models
#     if self.env.user.has_group('dp_hide_create_edit_button.group_hide_edit_button'):
#         temp = etree.fromstring(result['arch'])
#         temp.set('edit','0')
#         result['arch'] = etree.tostring(temp)
#
#     # hide Edit button in model
#     if self.env.user.hide_edit_model_ids:
#         models = self.env.user.hide_edit_model_ids
#         if self._name in models.mapped('model'):
#             temp = etree.fromstring(result['arch'])
#             temp.set('edit','0')
#             result['arch'] = etree.tostring(temp)
#
#     # hide write button on all models
#     if self.env.user.has_group('dp_hide_create_edit_button.group_hide_create_button'):
#         temp = etree.fromstring(result['arch'])
#         temp.set('create','0')
#         result['arch'] = etree.tostring(temp)
#
#     # hide create button in model
#     if self.env.user.hide_create_model_ids:
#         models = self.env.user.hide_create_model_ids
#         if self._name in models.mapped('model'):
#             temp = etree.fromstring(result['arch'])
#             temp.set('create','0')
#             result['arch'] = etree.tostring(temp)
#
#     return result
#
# BaseModel.fields_view_get = fields_view_get
