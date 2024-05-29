# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.osv import expression

class ShResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields):
        rec = super(ShResUsers, self).default_get(fields)

        journals = self.env.company.journal_ids.ids
        rec.update({
            'journal_ids' : [(6,0,journals)]
        })
        return rec

    journal_ids = fields.Many2many(
        'account.journal', string="Journals", copy=False)


class ShAccountJournalRestrict(models.Model):
    _inherit = 'account.journal'

    @api.model
    def default_get(self, fields):
        rec = super(ShAccountJournalRestrict, self).default_get(fields)

        users = self.env.company.sh_user_ids.ids
        rec.update({
            'user_ids' : [(6,0,users)]
        })
        return rec

    user_ids = fields.Many2many(
        'res.users', string="Users", copy=False)
    bypass_journal = fields.Boolean('Bypass Restriction', default=False)

    # To apply domain to action_________ 2
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        super(ShAccountJournalRestrict, self)._name_search(
            name, domain=domain, operator='ilike', limit=100, order=order)

        if(
            self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not
            (self.env.user.has_group("base.group_erp_manager"))
        ):
            domain += [
                ("user_ids", "in", self.env.user.id),('name','ilike',name)
            ]
        else:
            domain += [('name','ilike',name)]
        # return self._search(expression.AND([domains, domain]), limit=limit)
        return self._search(domain, limit=limit, order=order)

    # To apply domain to load menu_________ 1
    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        _ = self._context or {}
        if self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not self.env.user.has_group("base.group_erp_manager"):
            domain.append(("user_ids", "in", self.env.user.id))
        return super().search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )
