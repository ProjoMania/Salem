# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

{
    'name': 'Customer Type',
    'category': 'Accounting',
    'version': '0.1',
    'summary': 'Customer type in Account aged receivable, aged payable, partner ledger',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': 'http://www.technaureus.com/',
    'description': """ Customer type in Account aged receivable, aged payable, partner ledger""",
    # 'price': 79.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['account_reports', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/customer_type_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'tis_customer_type/static/src/xml/partner_filter.xml',
            # 'tis_customer_type/static/src/js/account_report.js',
        ],
    },
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
