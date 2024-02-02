
{
    "name": "Account Payment Mode",
    'version': '1.0',
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment",
    "category": "Banking addons",
    "license": "LGPL-3",
    "depends": ["base","account","account_accountant"],
    "data": [
        "security/account_payment_mode.xml",
        "security/ir.model.access.csv",
        "views/account_payment_method.xml",
        "views/account_payment_mode.xml",
        "views/account_journal.xml",
    ],
    "demo": [

        "demo/payment_demo.xml"

    ],
    "installable": True,
    "auto_install": False,
}
