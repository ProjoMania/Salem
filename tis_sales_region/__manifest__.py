# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

{
    'name': 'Sales Region',
    'version': '15.0.0',
    'category': 'Sales',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Sales Region',
    'description': """ Sales Region""",
    'website': 'http://www.technaureus.com',
    'price': 10,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_region_views.xml',
        'views/crm_team_views.xml',
    ],
    # 'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
}
