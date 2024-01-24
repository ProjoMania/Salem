# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': "aspl_aged_receivable_extend",

    'summary': """
        Account Aged Receivable Extend""",

    'description': """
        Account Aged Receivable Extend (Enterprise)
    """,

    'author': "Acespritech Solutions Pvt Ltd.",
    'website': "https://www.acespritech.com",


    'category': 'Accounting',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_accountant', 'account_reports'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/aged_receivable.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'aspl_aged_receivable_extend/static/src/js/account_receivable_extend.js',
        ],
    },

    }
