# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.
{
    'name': 'Odoo Employee Attandance Map',
    'summary': 'Get location of employee and load map using employee attendance location',
    'version': '15.0.0',
    'description': """Get location of employee and load map using employee attendance location""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'General',
    'website': "http://www.acespritech.com",
    'price': 20,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/templates.xml'
        'views/res_config_setting.xml',
        'views/hr_attendance_form_view.xml',
        'views/att_approval.xml',
    ],
    # 'qweb': [
    #     'static/src/xml/template.xml',
    # ],
    'assets': {
        'hr_attendance.assets_public_attendance': [
            'aspl_employee_attendance_map/static/src/xml/template.xml',
    #         'aspl_employee_attendance_map/static/src/js/main.js',
    #         'aspl_employee_attendance_map/static/src/js/view.js',
    #         'aspl_employee_attendance_map/static/src/js/customer_map.js'
        ],
    },
    'images': ['static/description/odoo12_5_select_department_and_employee.png'],
    'installable': True,
    'auto_install': False,
}
