# -*- coding: utf-8 -*-
{
    'name': 'stock_invoice',
    'summary': 'Shown Invoice on the stock move',
    'category': 'Utility',
    'description': """
        Shown Invoice on the stock move
    """,
    'author': 'Moashirat Consulting',
    'website': 'https://moashirat.com',
    'depends': ['stock', 'account'],
    'data': [

       'views/config_view.xml',
        'views/picking_view.xml',
          'views/account_move.xml',
    
    ],

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
