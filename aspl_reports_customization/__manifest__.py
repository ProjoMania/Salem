# -*- coding: utf-8 -*-
#############################################################################


{
    'name': 'Reports Customization',
    'version': '17.0.1.0.0',
    'category': 'Account/Sales/Website',
    'summary': 'Reports Customization',
    'description': 'QR code is added in header in pdf reports.',
    'author': '',
    'company': '',
    'images': [],
    'website': '',
    'depends': ['base', 'website', 'esco_account_report'],
    'data': [
        'views/report_header_view.xml',
        'views/report_template.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
