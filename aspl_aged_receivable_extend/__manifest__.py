# -*- coding: utf-8 -*-
{
    'name': "aspl_aged_receivable_extend",

    'summary': """
        Account Aged Receivable Extend""",

    'description': """
        Account Aged Receivable Extend (Enterprise)
    """,

    # 'author': "Acespritech Solutions Pvt Ltd.",
    # 'website': "https://www.acespritech.com",
    #

    'category': 'Accounting',
    'version': '17.0.0.1',
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_accountant', 'account_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/aged_receivable.xml',
        # 'views/templates.xml',
    ],
    'assets': {
        # 'web.assets_backend': [
        #     'aspl_aged_receivable_extend/static/src/js/account_receivable_extend.js',
        # ],
    },

    }
