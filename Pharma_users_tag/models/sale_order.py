from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        current_user = self.env.user
        if not self.env.user.has_group('base.group_erp_manager'):
            if current_user.partner_category_id:
                partner_tags = current_user.partner_category_id.ids
                domain += [('partner_id.category_id', 'in', partner_tags)]
        return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order, count_limit=count_limit)