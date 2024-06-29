# -*- coding: utf-8 -*-
#################################################################################

{
    'name': 'Pharma Contact Approval',

    'category': 'Uncategorized',
    
    'summary': 'This module allows to approve any changes in contact form.',
    
    'description': """This module allows to approve any changes in contact form""",
    
    'author': "My Company",
    
    'website': "https://www.yourcompany.com",
    
    'version': '0.1',
    
    'depends': ['base','sale_management', 'account_accountant', 'stock', 'account', 'contacts', 'purchase'],
    
    "data": [ 
        "views/res_partner_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}