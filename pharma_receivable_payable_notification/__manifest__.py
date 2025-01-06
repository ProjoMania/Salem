# -*- coding: utf-8 -*-
{
    'name': "Pharma Receivable and Payable Notification (Enterprise)",
    'summary': "Send notifications of pending payments",
    'description': """Send notifications of pending payments""",
    'license': 'LGPL-3',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "https://acespritech.com",
    'category': 'Accounting',
    'version': '17.0.1.0.0',
    'depends': ['base', 'account_accountant', 'contacts'],

    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
    ],
}

