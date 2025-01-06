# -*- coding: utf-8 -*-
{
    'name': "Pharma Competitors (Enterprise)",
    'summary': "Create competitors and customer classification",
    'description': """Create competitors and customer classification""",
    'license': 'LGPL-3',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "https://acespritech.com",
    'category': 'CRM',
    'version': '17.0.1.0.0',
    'depends': ['base','crm','stock','tis_customer_type'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/competitor_views.xml',
        'views/customer_classification_views.xml',
        'views/res_partner_inherted_views.xml',
    ],
    
    'installable': True,
    'application': True,
}

