# -*- coding: utf-8 -*-
{
    'name': 'Sale Analytic Account',
    'summary': 'Sale order line in add analytic account',
    'category': 'General',
    'description': """
        Sale order line in add analytic account
    """,
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['sale', 'account', 'analytic'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_analytic_account.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "aspl_sale_analytic_account/static/src/css/many2one_tag_widget.css",
            "aspl_sale_analytic_account/static/src/js/many2one_tag_widget.js",
            
        ],
        'web.assets_qweb': [
            "aspl_sale_analytic_account/static/src/xml/many2one_tag_widget.xml",
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
