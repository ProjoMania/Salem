# -*- coding: utf-8 -*-
{
    'name': "Quarantine and Released Picking Lots",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
block lots to be delivered to the customer till the lot is released, this dobale by check box on the delivery operation 
    """,

    'author': "Moashirat",
    'website': "https://moashirat.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'esco_medical_lot_approval'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

