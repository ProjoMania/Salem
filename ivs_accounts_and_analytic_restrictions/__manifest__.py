# -*- coding: utf-8 -*-
{
    'name': "Accounts and Analytic Restrictions",
    'summary': """Apply restrictions for Accounts and Analytic Accounts""",
    'description': """Restrict who can access the Accounts from the Chart of Accounts and the Analytic Accounts.
    """,
    'author': 'I Value Solutions',
    'website': 'www.ivalue-s.com',
    'email': 'info@ivalue-s.com',
    'license': 'OPL-1',
    'category': 'Accounting',
    'version': '0.1',
    'images': ['static/description/banner.jpg'],
    'price': 9.90,
    'currency': 'USD',
    # any module necessary for this one to work correctly
    'depends': ['base','account','analytic'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}