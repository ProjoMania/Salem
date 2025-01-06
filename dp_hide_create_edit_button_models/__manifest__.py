# -*- coding: utf-8 -*-
# DP InfoSol PVT LTD. See LICENSE file for full copyright and licensing details.
{
    'name'        : 'Hide Create/Edit Buttons globally or Model Base',
    'version'     : '14.0',
    "author"      : "DP InfoSol",
    "support"     : "help.dpinfosol@gmail.com",
    'category'    : 'Administration',
    'summary'     : '''This apps helps you restrict create edit buttons for users globally or model wise.''',
    'description' : """ user wise restriction
    restrict view user wise odoo
    if user have group he/she can't access create/edit button.
    security create,edit button
    how to hide create button in odoo
    hide edit button in odoo
    create/edit button in odoo
    hide create button and edit button in odoo
    Note: this will not work in many2one quick create. """,
    'depends'     : ['base', 'web'],
    'data'        : [
                    'security/security.xml',
                    'views/res_users.xml'
                    ],
    'installable' : True,
    'auto_install': False,
    "price"       : 15,
    "currency"    : "EUR",
    'license': 'LGPL-3',
    "images"      : ["static/description/banner.png",],
}
