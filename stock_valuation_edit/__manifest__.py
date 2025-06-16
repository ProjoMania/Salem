# -*- coding: utf-8 -*-
{
    'name': "Stock valuation edit",

    'summary': """
        Enables fix stock valuation""",

    'description': """
        Enables fix stock valuation
    """,

    'author': "Svyatoslav Nadozirny",

    'category': 'Inventory/Inventory',
    'version': '0.1',

    'depends': ['stock_account'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images':[
      'static/description/image1.png',
      'static/description/image2.png',
      'static/description/image3.png',
      'static/description/image4.png'

    ],

    'price': 2,
    'currency': 'EUR',
    'license': 'LGPL-3',

}
