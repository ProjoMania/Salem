# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

{
    'name': 'Viatris Sales Report',
    'version': '15.0.0.7',
    'category': 'Sales',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Sales report',
    'description': """ Viatris
Sale  Report
================================
    """,
    'website': 'http://www.technaureus.com',
    'price': 10,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['sale', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sales_region_wizard.xml',
        'wizard/excel_report.xml',
        # 'views/sale_region.xml',
        # 'views/crm_team.xml',
        'views/sales_region_report.xml',
        'views/stock_warehouse_views.xml',
    ],
    # 'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
}
