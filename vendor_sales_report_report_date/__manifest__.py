# -*- coding: utf-8 -*-
{
    'name': 'Vendor Sales Report By Report Date',
    'version': '2.1',
    'sequence': 1,
    'category': 'Sales',
    'summary': 'Vendor based xlsx sales report',
    'author': 'ahmed-youssef',
    'website': 'https://www.odoo.com',
    'price': '',
    'license': 'LGPL-3',
    'description': """Vendor based xlsx sales report""",
    'depends': ['sale_management', 'stock', 'contacts', 'product_expiry', 'sale','account_accountant', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',

        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'views/stock_move_lines_views.xml',
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
