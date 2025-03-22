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

from odoo import models, fields, api, _


class event_budget(models.Model):
    _name = 'event.budget'


    @api.depends('estimated_cost', 'actual_cost')
    def calculate_diff_amount(self):
        variance_amount = 0.00
        for record in self:
            variance_amount = record.estimated_cost - record.actual_cost
            record.write({'difference_cost': variance_amount})


    budget_id = fields.Many2one('budget.name', String="Budget Name")
    estimated_cost = fields.Float(string="Estimated Cost", tracking=True)
    actual_cost = fields.Float(string="Actual Cost", tracking=True)
    difference_cost = fields.Float(string="Variance", tracking=True, compute='calculate_diff_amount')
    event_id = fields.Many2one('event.event', string="Event")


class budget_name(models.Model):
    _name = 'budget.name'

    name = fields.Char('Name')
    event_buget_id = fields.Many2one('event.budget', string="Event Budget")
