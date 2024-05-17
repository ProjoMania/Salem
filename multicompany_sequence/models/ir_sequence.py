from odoo import api, fields, models


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _get_prefix_suffix(self, date=None, date_range=None):
        # if self.env.company.prefix:
        #     if not self.prefix:
        #         self.prefix = self.env.company.prefix
        #     else:
        #         companies_prefix = self.env['res.company'].search([]).mapped('prefix')
        #         # print('companies_prefix...', companies_prefix, self.prefix)
        #         if any(prefix and prefix in self.prefix for prefix in companies_prefix):
        #             for prefix in companies_prefix:
        #                 if prefix and prefix in self.prefix:
        #                     self.prefix = self.prefix.replace(prefix, self.env.company.prefix)
        #                     break
        #         else:
        #             # self.prefix = self.env.company.prefix + "-" + self.prefix
        #             self.prefix = self.env.company.prefix + self.prefix
        interpolated_prefix, interpolated_suffix = super(IrSequence, self)._get_prefix_suffix(date=date, date_range=date_range)
        if self.env.company.prefix:
            interpolated_prefix = str(self.env.company.prefix) + str(interpolated_prefix)
        return interpolated_prefix, interpolated_suffix
