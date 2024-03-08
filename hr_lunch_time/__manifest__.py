# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hr Attendance Lunch Time',
    'version': '17.0.1.1',
    'category': 'Human Resources/Attendances',
    'author': 'Dev JS',
    'sequence': 99,
    'summary': 'Lunch Start Time And End Time  Hr Attendance',
    'depends': [
        'hr',
        'hr_attendance',
    ],
    'data': [
        'views/hr_attendance.xml',
    ],
    'assets': {
        'web.assets_backend': [
           'hr_lunch_time/static/src/js/attendance_menu.js',
        #    'hr_lunch_time/static/src/js/kiosk_face_recognition.js',
        #    'hr_lunch_time/static/src/js/kiosk_mode.js',
            'hr_lunch_time/static/src/xml/menu.xml',
        ],
    },
    'demo': [],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/attendance.xml',
    ],
    'application': True,
    'price': 15,
    'currency': 'EUR',
    'license': 'LGPL-3',
}
