# -*- coding: utf-8 -*-
{
    'name': "Schedule Activity Access",
    'summary': """ Allow only assign user to edit the schedule activity  """,
    'description': """
        - The schedule activity will be visible to the one who has access
        to the document.
        - The created user of the activity can't make any changes ones the
        activity is created.
        - The user to whom the activity is assigned can make changes in the
        assign activity.
    """,
    'author': "Aktiv Software",
    'website': "www.aktivsoftware.com",
    'category': 'Discuss',
    'version': '14.0.1.0.5',
    'depends': ['sale_management'],
    'data': [
        'security/activity_security.xml',
        # 'views/sale_order_view.xml',
    ],
    'qweb': [
        # 'static/src/xml/activity.xml',
        # 'static/src/xml/hide.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
