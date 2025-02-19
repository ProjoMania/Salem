# -*- coding: utf-8 -*-
from odoo import models

class IrUiView(Model):
    _inherit = 'ir.ui.view'

    def _get_view(self, view_id=None, view_type=None, **options):
        arch, view = super(IrUiView, self)._get_view(view_id, view_type, **options)
        
        # by pass for root user
        if self.env.uid == 1:
            return arch, view
            
        app_check = self.env['ir.module.module'].search([('name','=','dp_hide_create_edit_button_models')], limit=1)
        if app_check:
            if app_check.state != 'installed':
                return arch, view

        # Determine if edit button should be hidden based on user groups and model settings
        should_hide_edit = False
        
        # Check if user has group-level edit restriction
        if self.env.user.has_group('dp_hide_create_edit_button_models.group_hide_edit_button'):
            should_hide_edit = True
            
        # Check if current model is in user's model-specific edit restrictions
        if self.env.user.hide_edit_model_ids:
            if self._name in self.env.user.hide_edit_model_ids.mapped('model'):
                should_hide_edit = True
                
        # Set edit attribute based on restrictions
        arch.set('edit', '0' if should_hide_edit else '1')

        # Determine if create button should be hidden based on user groups and model settings
        should_hide_create = False
        
        # Check if user has group-level create restriction
        if self.env.user.has_group('dp_hide_create_edit_button_models.group_hide_create_button'):
            should_hide_create = True
            
        # Check if current model is in user's model-specific create restrictions
        if self.env.user.hide_create_model_ids:
            if self._name in self.env.user.hide_create_model_ids.mapped('model'):
                should_hide_create = True
                
        # Set create attribute based on restrictions
        arch.set('create', '0' if should_hide_create else '1')

        return arch, view
