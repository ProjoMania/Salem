# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.
import datetime

from odoo import models, fields


class AttApproval(models.TransientModel):
    _name = 'att.approval'
    _rec_name = 'employee_name'

    employee_name = fields.Many2one('hr.employee', readonly=True)

    date = fields.Datetime(default=datetime.datetime.now(), readonly=True)
    latitude = fields.Float(digits=(12, 7))
    longitude = fields.Float(digits=(12, 7))
    browser_name = fields.Char()
    os_name = fields.Char()
    state = fields.Selection(
        [
            ("pending", "Pending "),
            ("approved", "Approved"),

        ],
        string="State",
        default="pending",
    )
    in_or_out=fields.Boolean()
    status=fields.Char()

    employee_location = fields.Char(string="Employee Location", required=True, readonly=True)

    def att_approve(self):
        self.state = 'approved'
        print(self.status)
        if self.status=='checked_out':
            vals = {
                'employee_id': self.employee_name.id,
                'check_in': datetime.datetime.now()
            }

            vals.update({
                'longitude': self.longitude,
                'latitude': self.latitude,
                'os_name': self.os_name,
                'browser_name': self.browser_name,
                'location_name': self.employee_location,
            })
            att = self.env['hr.attendance'].sudo().create(vals)
        else:
            attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', self.env.user.employee_id.id), ('check_out', '=', False)],
                limit=1)
            if attendance:
                attendance.check_out = datetime.datetime.now()
