# -*- coding: utf-8 -*-
{
    'name': 'Stock Landed Costs Account Fix',
    'version': '1.0',
    'summary': 'Fixes NULL account_id issue in stock landed costs',
    'description': '''
        This module fixes an issue in the stock_landed_costs module where NULL account_id values 
        can be created in account.move.line records, violating database constraints.
        
        The fix ensures that all account move lines created for landed costs always have a valid account_id.
    ''',
    'category': 'Inventory/Inventory',
    'author': 'Salem',
    'website': '',
    'depends': ['stock_landed_costs'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
