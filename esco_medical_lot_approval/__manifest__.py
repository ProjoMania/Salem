# -*- coding: utf-8 -*-
{
    'name': 'Medical Batch Approval Process',
    'summary': 'Moashirat',
    'category': 'Inventory',
    'description': """
        Medical Batch Approval Process
    """,
    'sequence': 1,
    'author': 'Moshirat Consulting',
    'website': 'https:/moashirat.com',
    'depends': ['stock', 'product_expiry'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_production_lot_views.xml',
        'views/stock_move_view.xml',
        'views/stock_quant_view.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',

}
