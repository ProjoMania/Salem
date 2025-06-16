from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def default_get(self, fields):
        res = super(ProductProduct, self).default_get(fields)
        res['company_id'] = self.env.company.id
        return res

    @api.constrains('company_id')
    def _check_company_id(self):
        for rec in self:
            if not rec.company_id:
                raise ValidationError(_('The company must be set for the product.')) 