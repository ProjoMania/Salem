{
    'name': 'Validate Float Fields',
    'version': '17.0.1.0.0',
    'category': 'Stock',
    'summary': 'Warn if scrap_qty in stock.scrap is not an integer value',
    'description': """
        This module raises a warning if the field 'scrap_qty' in the model 'stock.scrap' is set to a non-integer value.
        Only values like 2, 2.00 are accepted. Values like 2.1, 2.01, 2.0000001 are not accepted.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['stock'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
} 