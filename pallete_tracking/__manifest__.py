# -*- coding: utf-8 -*-

{
    'name': 'ASPL: Pallets Tracking',
    'version': '17.0.1.0.0',
    'description': """
        ASPL: Pallets Tracking""",
    'currency': 'EUR',
    'license': 'LGPL-3',
    'summary': 'ASPL: Pallets Tracking',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/amcl_manager_groups.xml',
        # 'wizards/so_line_wizard.xml',
        'views/data_loggger_view.xml',
        'views/data_logger_form_view.xml',
    ],

    'installable': True,
    'auto_install': False,
}
