from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo import http
from odoo.http import request


class HrAttendanceLunch(HrAttendance):

    @staticmethod
    def _get_employee_info_response(employee):
        res = super(HrAttendanceLunch, HrAttendanceLunch)._get_employee_info_response(employee)
        if res and employee:
            res.update({
                'lunch_start': employee.last_attendance_id.lunch_start,
                'lunch_end': employee.last_attendance_id.lunch_end,
            })
        return res

    @http.route()
    def systray_attendance(self, latitude=False, longitude=False, **post):
        employee = request.env.user.employee_id
        geo_ip_response = self._get_geoip_response(mode='systray',
                                                   latitude=latitude,
                                                   longitude=longitude)
        employee._attendance_action_change(geo_ip_response, **post)
        return self._get_employee_info_response(employee)
