# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.


import httpagentparser
from odoo import fields, models, api, _, exceptions
from odoo.http import request
from datetime import datetime
import logging, requests, platform
from geopy.geocoders import Nominatim

from odoo.tools.safe_eval import json

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_api_key = fields.Char(string='Google API KEY')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(google_api_key=self.env['ir.config_parameter'].sudo().get_param(
            'aspl_employee_attendance_map.google_api_key'))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('aspl_employee_attendance_map.google_api_key',
                                                         self.google_api_key)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_name = fields.Char(string="Location Name")
    latitude = fields.Char(string="latitude")
    longitude = fields.Char(string="Logitude")
    os_name = fields.Char(string="Operationg System")
    browser_name = fields.Char(string="Browser")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_inside = fields.Boolean()

    def inside_poly(self, val):
        print(val)
        self.sudo().is_inside = val
        print(1, "a")

    def search_lat_lng(self):
        emp_ids = self.env['emp.lat.lng.info'].search([('employee_id', '=', self.id)])
        records = {}
        for emp in emp_ids:
            for rec in emp.lat_lng_ids:
                if emp.id not in records:
                    records[emp.id] = [
                        {'latitude': rec.latitude, 'longitude': rec.longitude, 'id': rec.emp_lat_lng_id.id}]
                else:
                    records[emp.id].append(
                        {'latitude': rec.latitude, 'longitude': rec.longitude, 'id': rec.emp_lat_lng_id.id})
        return records

    def store_lat_lng(self, array):
        if array:
            self.env['emp.lat.lng.info'].create({
                'employee_id': self.id,
                'lat_lng_ids': [[0, 0, {
                    'latitude': each.get('lat'),
                    'longitude': each.get('lng'),
                }] for each in array]
            })

    def delete_lat_lng(self, emp_lat_id):
        if emp_lat_id:
            self.env['emp.lat.lng.info'].browse([int(emp_lat_id)]).unlink()
            return True

    def attendance_manual(self, next_action, entered_pin=None, latitude=None, longitude=None):
        print(2)
        if self.is_inside == False:
            geolocator = Nominatim(user_agent="aspl_employee_attendance_map")
            agent = request.httprequest.environ.get('HTTP_USER_AGENT')
            agent_details = httpagentparser.detect(agent)
            browser_name = agent_details['browser']['name']
            location = geolocator.reverse("%s, %s" % (latitude, longitude))
            user_os = agent_details['os']['name']
            bit_type = platform.architecture()
            self.env['att.approval'].create({
                'employee_name': self.env.user.employee_id.id,
                'employee_location': location.address,
                'latitude': latitude,
                'longitude': longitude,
                'browser_name': browser_name,
                'os_name': user_os + ", " + bit_type[0],
                'in_or_out': self.is_inside,
                'status': self.attendance_state,

            })

            # subject = "Need Attendance Approval"
            #
            # mail_body = (
            #
            #         "Dear %s,<br/><br/>"
            #         "I hope this email finds you well. I am writing to get approval for Location %s,"
            #         % (
            #             self.env.user.employee_id.parent_id.name, location.address)
            #
            # )
            # email_from = self.env.user.employee_id.work_email
            # email_to = self.env.user.employee_id.parent_id.work_email
            # self.env["mail.mail"].sudo().create(
            #     {
            #         "email_from": email_from,
            #         "author_id": self.env.user.partner_id.id,
            #         "body_html": mail_body,
            #         "subject": subject,
            #         "email_to": email_to,
            #         # "email_cc": email_cc,
            #         "auto_delete": True,
            #     }
            # ).send()
            return None
        else:
            return self.attendance_action(next_action, entered_pin, latitude, longitude)

    def attendance_action(self, next_action, entered_pin=None, latitude=None, longitude=None):
        self.ensure_one()
        action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').sudo().read()[0]
        action_message['previous_attendance_change_date'] = self.last_attendance_id and (
                self.last_attendance_id.check_out or self.last_attendance_id.check_in) or False
        action_message['employee_name'] = self.name
        action_message['next_action'] = next_action
        if self.user_id:
            modified_attendance = self.sudo(self.user_id.id).attendance_action_change(latitude, longitude)
        else:
            modified_attendance = self.sudo().attendance_action_change(latitude, longitude)
        if modified_attendance:
            action_message['attendance'] = modified_attendance.read()[0]
            return {'action': action_message}

    def attendance_action_change(self, latitude=None, longitude=None):
        emp_ids = self.env['emp.lat.lng.info'].search([('employee_id', '=', self.id)])
        if not emp_ids:
            raise exceptions.UserError("Please Add Allowed Check in Location")

        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        action_date = fields.Datetime.now()
        agent = request.httprequest.environ.get('HTTP_USER_AGENT')
        agent_details = httpagentparser.detect(agent)
        user_os = agent_details['os']['name']
        browser_name = agent_details['browser']['name']
        bit_type = platform.architecture()
        geolocator = Nominatim(user_agent="aspl_employee_attendance_map")
        state = self._context.get('state')
        print(state, self.attendance_state, "state")

        if self.attendance_state == 'checked_out' and state != 'lunch_end':
            print("jjj")
            vals = {
                'employee_id': self.id,
                'check_in': action_date
            }
            location = geolocator.reverse("%s, %s" % (latitude, longitude))
            vals.update({
                'longitude': longitude,
                'latitude': latitude,
                'os_name': user_os + ", " + bit_type[0],
                'browser_name': browser_name,
                'location_name': location.address,
            })
            return self.env['hr.attendance'].create(vals)

        attendance = self.env['hr.attendance'].search(
            [('employee_id', '=', self.id), ('check_out', '=', False)],
            limit=1)
        if attendance and state:
            if state == 'lunch_start':
                attendance.lunch_start = action_date
            elif state == 'lunch_end':
                attendance.lunch_end = action_date
            elif state == 'check_out':
                attendance.check_out = action_date
        elif attendance and not state:
            attendance.check_out = action_date
        else:
            raise exceptions.UserError(
                ('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                 'Your attendances have probably been modified manually by human resources.') % {
                    'empl_name': self.name, })
        return attendance


class EmployeeAttendanceMap(models.Model):
    _name = 'employee.attendance.map'
    _rec_name = 'r_name'
    _description = "Generate Google Map based On Parameters"

    employee_ids = fields.Many2many('hr.employee', string="Employees", store=True)
    attendance_date = fields.Date(string="Date", required=True, default=datetime.today())
    department_id = fields.Many2one('hr.department', string="Department")
    job_position = fields.Many2one('hr.job', string="Job Position")
    r_name = fields.Char(default="Employee Attendance Map")

    @api.onchange('employee_ids', 'department_id', 'attendance_date', 'job_position')
    def employee_id(self):
        id_one = self.env['employee.attendance.map'].browse(1)
        id_one.department_id = self.department_id
        id_one.attendance_date = self.attendance_date
        id_one.job_position = self.job_position
        ls = []
        if self.employee_ids:
            for employee_id in self.employee_ids:
                id = str(employee_id).split('=')
                id = id[1].split('>')
                id = int(id[0])
                ls.append(id)
            emp_id = self.env['hr.employee'].search([('id', 'in', ls)])
            id_one.employee_ids = emp_id
        else:
            emp_id = self.env['hr.employee'].search([('id', '=', '00')])
            id_one.employee_ids = emp_id

    def show_map(self):
        print(self.employee_ids.name, self.department_id.name, self.attendance_date, self.job_position, "hh")
        try:
            response = requests.get("http://www.google.com")
            check_connection = True
        except requests.ConnectionError:
            check_connection = False
        attendance_obj = self.env['hr.attendance']
        result = []
        result.append({'connection': check_connection})

        domain = []
        if self.employee_ids:
            domain += [('id', 'in', self.employee_ids.ids)]
        if self.department_id:
            domain += [('department_id', '=', self.department_id.id)]
        if self.job_position:
            domain += [('job_id', '=', self.job_position.id)]

        employee_ids = self.env['hr.employee'].search(domain)
        if employee_ids:
            emp_detail = attendance_obj.search([('employee_id', 'in', employee_ids.ids)])
            for each_emp in emp_detail:
                emp_date = datetime.strptime(str(each_emp.check_in), '%Y-%m-%d %H:%M:%S')
                select_date = datetime.strptime(str(self.attendance_date), '%Y-%m-%d')
                new_emp_date = datetime.date(emp_date)
                new_select_date = datetime.date(select_date)
                if new_emp_date == new_select_date:
                    result.append({'latitude': each_emp.latitude,
                                   'longitude': each_emp.longitude,
                                   'os_name': each_emp.os_name,
                                   'name': each_emp.employee_id.name,
                                   'emp_id': each_emp.employee_id.id,
                                   'image': each_emp.employee_id.image_1920,
                                   'date': self.attendance_date,
                                   'dept_id': self.department_id.id,
                                   'job_position': self.job_position.id
                                   })
                else:
                    continue
        return result

    def employee_attendance(self, id, at_date, dept_id, job_position):
        lst = []
        filter_domain = "[('id','in',"
        emp_attendance = request.env['hr.attendance'].search([('employee_id', '=', int(id))])
        for each_emp in emp_attendance:
            emp_date = datetime.strptime(str(each_emp.check_in), '%Y-%m-%d %H:%M:%S')
            select_date = datetime.strptime(str(at_date), '%Y-%m-%d')
            new_emp_date = datetime.date(emp_date)
            new_select_date = datetime.date(select_date)
            if new_emp_date == new_select_date:
                if each_emp:
                    lst.append(each_emp.id)
                else:
                    filter_domain = ""
        filter_domain += "[" + ','.join(map(str, lst)) + "]"
        filter_domain += ")]"
        return json.dumps({'filter_domain': filter_domain})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
