
{
    'name': 'Pharma Maximum Quantity Approval',
    'category': 'Sale',
    'version': '0.1',
    'summary': '',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': '',
    'description': """ """,
    # 'price': 0.0,
    'currency': 'EUR',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'pharma_sales_rep'],
    'data': [
        'views/res_users_view.xml',
        'views/sale_order_view.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
