# -*- coding: utf-8 -*-
#################################################################################

{
    'name': 'Invoice Report',

    'category': 'Uncategorized',
    
    'summary': 'This module allows custom Invoice Report.',
    
    'description': """Custom report for Invoice.""",
    
    'author': "My Company",
    
    'website': "https://www.yourcompany.com",
    
    'version': '0.1',
    
    'depends': ['base','account','account_accountant','stock','pharma_discount_approval'],
    
    "data": [
        'views/res_partner_view.xml',
        'report/invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}