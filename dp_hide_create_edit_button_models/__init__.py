# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
from . import models
from odoo.addons.base.models.ir_ui_view import Model
from lxml import etree

get_view_super = Model._get_view

def _get_view(self, view_id=None, view_type=None, **options):
    result = get_view_super(self, view_id=view_id, view_type=view_type, **options)
    
    # by pass for root user
    if self.env.uid == 1:
        return result
        
    app_check = self.env['ir.module.module'].search([('name','=','dp_hide_create_edit_button_models')], limit=1)
    if app_check:
        if app_check.state != 'installed':
            return result

    # hide create button on all models
    if self.env.user.has_group('dp_hide_create_edit_button.group_hide_edit_button'):
        temp = etree.fromstring(result['arch'])
        temp.set('edit','0')
        result['arch'] = etree.tostring(temp)

    # hide Edit button in model
    if self.env.user.hide_edit_model_ids:
        models = self.env.user.hide_edit_model_ids
        if self._name in models.mapped('model'):
            temp = etree.fromstring(result['arch'])
            temp.set('edit','0')
            result['arch'] = etree.tostring(temp)

    # hide write button on all models
    if self.env.user.has_group('dp_hide_create_edit_button.group_hide_create_button'):
        temp = etree.fromstring(result['arch'])
        temp.set('create','0')
        result['arch'] = etree.tostring(temp)

    # hide create button in model
    if self.env.user.hide_create_model_ids:
        models = self.env.user.hide_create_model_ids
        if self._name in models.mapped('model'):
            temp = etree.fromstring(result['arch'])
            temp.set('create','0')
            result['arch'] = etree.tostring(temp)

    return result

Model._get_view = _get_view
