# -*- coding: utf-8 -*-
#################################################################################

{
    'name': 'Pharma Sale Expense (Enterprise)',
    'category': 'Uncategorized',
    'summary': 'This module allows to show hr expense in sale.',
    'description': """This module allows hr expense to show in sale""",
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "https://acespritech.com",
    'version': '17.0.1.0.0',
    'depends': ['base','hr_expense','sale_management', 'stock'],
    
    "data": [
        "views/hr_expense.xml",
        "views/account_move_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}