# -*- coding: utf-8 -*-

{
    'name': 'ASPL: Sales Order Quick Preview',
    'version': '17.0.1.0.0',
    'description': """
        ASPL: Sales Order Quick Preview""",
    'currency': 'EUR',
    'license': 'LGPL-3',
    'summary': 'ASPL: Sales Order Quick Preview',
    'depends': ['base', 'sale', 'sale_management', 'payment', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'security/amcl_manager_groups.xml',
        'wizards/so_line_wizard.xml',
        'views/sale.order.xml',
    ],

    'installable': True,
    'auto_install': False,
}
