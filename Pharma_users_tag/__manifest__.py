# -*- coding: utf-8 -*-
#################################################################################

{
    'name': 'Pharma User Tag (Enterprise)',

    'category': 'Uncategorized',
    
    'summary': 'User Tags',
    
    'description': """This module allows to add tags in user.""",
    
    'author': "My Company",
    
    'website': "https://www.yourcompany.com",
    
    'version': '0.1',
    
    'depends': ['base','account','account_accountant','sale_management','stock'],
    
    "data": [
        "views/res_users_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

