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
    'name': 'Event Management',
    'category': 'General',
    'description': """Manage the events.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base','event', 'hr', 'product','stock'],
    'data': [
        'security/event_security.xml',
        'views/reject_reason_view.xml',
        'views/event_event_views.xml',
        'data/event_data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: