
{
    "name": "Bank from IBAN",
    "version": "1.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "category": "Localization",
    "license": "AGPL-3",
    "depends": ["base_iban"],
    "development_status": "Mature",
    "data": ["views/res_bank_view.xml"],
    "external_dependencies": {"python": ["schwifty"]},
    "installable": True,
}
