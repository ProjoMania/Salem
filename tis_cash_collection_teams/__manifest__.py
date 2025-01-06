# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.

{
    'name': 'Cash Collection Teams',
    'version': '15.0.0',
    'summary': 'Cash Collection Teams For Invoice',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'description': 'Cash Collection Teams For Invoice',
    'website': 'http://www.technaureus.com',
    'license': 'Other proprietary',
    'depends': ['account', 'account_accountant'],
    'data': [
        'security/cash_collection_security_groups.xml',
        'security/ir.model.access.csv',
        'views/cash_collection_team_views.xml',
        'views/res_partner_form_inherit.xml',
    ],
    'assets': {},
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
