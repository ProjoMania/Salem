# -*- coding: utf-8 -*-
from odoo import models
import logging

_logger = logging.getLogger(__name__)

class Model(models.AbstractModel):
    _inherit = 'base'

    def _get_view(self, view_id=None, view_type=None, **options):
        arch, view = super(Model, self)._get_view(view_id, view_type, **options)
        
        # by pass for root user
        if self.env.uid == 1:
            _logger.info('Root user detected - bypassing button restrictions')
            return arch, view
            
        app_check = self.env['ir.module.module'].search([('name','=','dp_hide_create_edit_button_models')], limit=1)
        if app_check:
            if app_check.state != 'installed':
                _logger.info('Module not installed - bypassing button restrictions')
                return arch, view

        # Determine if edit button should be hidden based on user groups and model settings
        should_hide_edit = False
        
        # Check if user has group-level edit restriction
        if self.env.user.has_group('dp_hide_create_edit_button_models.group_hide_edit_button'):
            _logger.info('User %s has group-level edit restriction', self.env.user.name)
            should_hide_edit = True
            
        # Check if current model is in user's model-specific edit restrictions
        if self.env.user.hide_edit_model_ids:
            if self._name in self.env.user.hide_edit_model_ids.mapped('model'):
                _logger.info('Model %s is in user %s model-specific edit restrictions', self._name, self.env.user.name)
                should_hide_edit = True
                
        # Set edit attribute based on restrictions
        arch.set('edit', '0' if should_hide_edit else '1')
        _logger.info('Edit button visibility set to %s for user %s on model %s', 
                    'hidden' if should_hide_edit else 'visible', 
                    self.env.user.name, 
                    self._name)

        # Determine if create button should be hidden based on user groups and model settings
        should_hide_create = False
        
        # Check if user has group-level create restriction
        if self.env.user.has_group('dp_hide_create_edit_button_models.group_hide_create_button'):
            _logger.info('User %s has group-level create restriction', self.env.user.name)
            should_hide_create = True
            
        # Check if current model is in user's model-specific create restrictions
        if self.env.user.hide_create_model_ids:
            if self._name in self.env.user.hide_create_model_ids.mapped('model'):
                _logger.info('Model %s is in user %s model-specific create restrictions', self._name, self.env.user.name)
                should_hide_create = True
                
        # Set create attribute based on restrictions
        arch.set('create', '0' if should_hide_create else '1')
        _logger.info('Create button visibility set to %s for user %s on model %s', 
                    'hidden' if should_hide_create else 'visible', 
                    self.env.user.name, 
                    self._name)

        return arch, view
