# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2023. All rights reserved.
{
    'name': 'Restrict Partner Invoice',
    'version': '15.0.0',
    'category':
        'sale', 'invoicing'
    'summary': 'Restrict partner invoice',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'license': 'LGPL-3',
    'description': """ 
        invoice due date blocking
    """,
    'depends': ['sale', 'account'],
    'data': [
             'security/security.xml',
             'views/partner.xml',
             'views/sale_order_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False
}
