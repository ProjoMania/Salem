
{
    'name': 'Pharma Stock',
    'category': 'Stock',
    'version': '0.1',
    'summary': '',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': '',
    'description': """ """,
    'currency': 'EUR',
    'license': 'LGPL-3',
    'depends': ['base', 'stock', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_location_view.xml',
        'views/liq_location_view.xml',
        'views/res_partner_view.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
