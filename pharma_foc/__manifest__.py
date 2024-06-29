# -*- coding: utf-8 -*-
{
    'name': "Pharma FOC (Enterprise)",
    'summary': "Provide FOC products",
    'description': """Provide free of cost products""",
    'license': 'LGPL-3',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "https://acespritech.com",
    'category': 'Sales',
    'version': '17.0.1.0.0',
    'depends': ['base', 'sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_inherited_views.xml',
        'views/foc_product_views.xml',
        'views/sale_order_inherited_views.xml',
    ],
}

