# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.


from odoo import fields, models


class LatitudeLongitudeInformation(models.Model):
    _name = 'lat.lng.info'
    _description = "Store Latitude Longitude Information"

    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Logitude")
    emp_lat_lng_id = fields.Many2one('emp.lat.lng.info', string="Lat Lng", ondelete='cascade')


class EmployeeLatitudeLongitudeInformation(models.Model):
    _name = 'emp.lat.lng.info'
    _description = "Store Employee Latitude Longitude Information"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    lat_lng_ids = fields.One2many('lat.lng.info', 'emp_lat_lng_id', string="Lat Lng")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
