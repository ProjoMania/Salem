# -*- coding: utf-8 -*-
{
    'name': "Shipment Document Tracking",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """Long description of module's purpose """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','mail','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',

        'data/sequence.xml',
        'data/mail_activity_type_data.xml',
        'views/doc_doc_views.xml',
        'views/res_partner_views.xml',
        'views/shipment_doc_tracking.xml',
        'views/config.xml',
        'views/purchase_order.xml',
        'views/move.xml',
        'wizard/billing_wiz.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}

