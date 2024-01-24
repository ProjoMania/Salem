# -*- coding: utf-8 -*-
{
    "name": "Print Journal Entries",

    "author": "Softhealer Technologies",

    "license": "OPL-1",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "14.0.2",

    "category": "Accounting",

   	"summary": "print journal report app, print multiple journal module, print journal entry, Print Journal Entries, Print Journals, Journals Report, Journals Entries, Journals Entry odoo",

   	"description": """This module useful to print journal entries.""",

   	"depends":  ['account'],

   	"data": [
            "security/ir.model.access.csv",
            "reports/report_account_journal_entries.xml",
            "wizard/journal_entries_xls_report_wizard.xml",
        ],
   	"images": ["static/description/background.png", ],

   	"installable": True,
   	"application": True,
   	"auto_install": False,
    "live_test_url": "https://youtu.be/UvHv24t9d1U",
   	"price": 8,
   	"currency": "EUR"

}
