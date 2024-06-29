
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    visit_id = fields.Many2one('visit.order', string='Visit')
    drug_store_id = fields.Many2one('res.partner', string='Drug Store')

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            for node in arch.xpath("//tree/field[@name='product_template_id']"):
                existing_context = node.get('context', '{}')
                new_context = "{'product_category': True}"
                merged_context = f"{existing_context[:-1]}, {new_context[1:]}" if existing_context != '{}' else new_context
                node.set('context', merged_context)
        return arch, view


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        user = self.env.user
        if not self.env.user.has_group('base.group_erp_manager'):
            if self._context.get('product_category'):
                category_ids = user.product_category_ids.ids
                product_templates = self.search([('categ_id', 'in', category_ids)])
                args += [('id', 'in', product_templates.ids)]
        return super(ProductTemplate, self).name_search(name, args=args, operator=operator, limit=limit)


# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     @api.model
#     def name_search(self, name, args=None, operator='ilike', limit=100):
#         if not args:
#             args = []
#         user = self.env.user
#         if user.product_category_ids:
#             category_ids = user.product_category_ids.ids
#             product_templates = self.env['product.template'].search([('categ_id', 'in', category_ids)])
#             args += [('product_tmpl_id', 'in', product_templates.ids)]
#         return super(ProductProduct, self).name_search(name, args=args, operator=operator, limit=limit)
