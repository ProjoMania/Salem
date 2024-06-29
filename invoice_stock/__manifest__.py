{
    'name': 'Print Invoice from Delivery Order',
    'version': '1.0.0',
    'depends': ['stock'],
    'author': 'Your Name/Company',
    'category': 'Sale',
    'description': """
        This module adds a button to the delivery order form that allows users to print the linked invoice.
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/delivery_order_print_invoice_button.xml',
    ],
    'installable': True,
}