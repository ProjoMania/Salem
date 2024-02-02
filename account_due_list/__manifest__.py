{
    'name': "Payments Due list",
    'version': '1.0',
    "license": "LGPL-3",
    "depends": ["base","account","account_accountant"],
    "category": "Generic Modules/Payment",
    "development_status": "Production/Stable",
    "author": "Odoo Community Association (OCA)",
    "summary": "List of open credits and debits, with due date",
    "website": "https://github.com/OCA/account-payment",
    "data": [
        "views/payment_view.xml"
    ],

    'demo': [],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
    "auto_install": False,
}

