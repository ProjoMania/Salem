# -*- coding: utf-8 -*-
{
    'name': 'BAIT Reports Design',
    'summary': 'New Reports Design for BAIT',
    'category': 'Utility',
    'description': """
        Custom reports for BAIT
    """,
    'author': 'Engineering Solutions ESCO',
    'website': 'www.escoiq.com',
    'depends': ['account', 'report_xlsx', 'sale', 'reports_with_watermark', 'stock', 'purchase',
                'esco_num2word_arabic','account_reports'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'wizard/report_partner_wiz.xml',
        'report/report_layout_view.xml',
        'report/report_payment_receipt.xml',
        'report/report_customer_statement.xml',
        'report/report_purchase_order.xml',
        'report/report_request_for_quotation.xml',
        'report/report_delivery_slip.xml',
        'report/report_invoice.xml',
        'report/report_sale_order.xml',
        'report/report_view.xml',
        'views/res_users_view.xml',
        'views/config_view.xml',
        'views/purchase_view.xml',
        'views/res_partner_view.xml',
        'views/payment_view.xml',
        'views/account_move.xml',
        'views/picking_view.xml',
        'views/company.xml'
    ],
    "assets": {
        "web.assets_backend": [
            "esco_account_report/static/src/css/font.css",
            "esco_account_report/static/src/css/style.css",
        ],
        "web.assets_common": [
            "esco_account_report/static/src/css/font.css",
        ],
        "web.report_assets_common": [
            "esco_account_report/static/src/css/font.css",
            "esco_account_report/static/src/less/fonts.less",
            "esco_account_report/static/src/css/style.css",
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
