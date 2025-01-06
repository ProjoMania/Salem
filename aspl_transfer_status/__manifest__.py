# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    "name" : "ASPL Tranfer Status (Enterprise)",
    'summary' : "ASPL Tranfer Status (Enterprise)",
    "version" : "1.0",
    "description": """ASPL Tranfer Status""",
    'author' : 'Acespritech Solutions Pvt. Ltd.',
    'category' : 'stock',
    'website' : 'http://www.acespritech.com',
    'price': 30,
    'currency': 'EUR',
    'images': '',
    "depends": ['base', 'stock'],
    "data": [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/transfer_status_view.xml',
        'views/transfer_status_state_view.xml',
        'views/stock_picking_views.xml',
    ],
    "license" : 'LGPL-3',
    "auto_install": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: