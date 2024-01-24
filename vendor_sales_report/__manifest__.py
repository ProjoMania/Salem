# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

{
    'name': 'Vendor Sales Report',
    'version': '15.0.0.7',
    'sequence': 1,
    'category': 'Sales',
    'summary': 'Vendor based xlsx sales report',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'price': '',
    'currency': 'EUR',
    'license': 'Other proprietary',
    'description': """Vendor based xlsx sales report""",
    'depends': ['sale_management', 'stock', 'contacts', 'product_expiry', 'sale', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/vendor_sales_report_cron.xml',
        'data/vendor_sales_report_email_template.xml',
        'views/res_partner_form_view_inherit.xml',
        'views/sale_order_views.xml',
        'views/report_menu.xml',
        'wizard/vendor_sales_report.xml',
        'wizard/excel_report.xml',
    ],
    'images': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
    },
}
