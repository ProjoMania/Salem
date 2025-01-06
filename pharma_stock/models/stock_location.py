
from odoo import models, fields, api
from odoo.exceptions import UserError


class Location(models.Model):
    _name = "stock.location"
    _inherit = ['stock.location', 'mail.thread', 'mail.activity.mixin']

    min_qty = fields.Integer(string='Minimum Quantity')
    max_qty = fields.Integer(string='Maximum Quantity')
    sales_rep = fields.Many2one('res.users', string="Sales Rep")
    is_liquidation = fields.Boolean(string="Is Liquidation Location")
    is_drug = fields.Boolean(string="Is Drug Stock")


class StockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant', 'mail.thread', 'mail.activity.mixin']

    def write(self, vals):
        res = super().write(vals)
        locations = self.mapped('location_id')
        for location in locations:
            total_stock = sum(self.search([('location_id', '=', location.id)]).mapped('quantity'))
            model_id = self.env['ir.model']._get(self._name).id
            if total_stock <= location.min_qty:
                activity_id = self.env['mail.activity'].create({
                    'display_name': 'Minimum Stock',
                    'summary': 'This product has reached the minimum level of the stock.',
                    'res_id': location.id,
                    'res_model_id': model_id,
                })
            elif total_stock >= location.max_qty:
                if not self.env.user.has_group('base.group_erp_manager'):
                    raise UserError('Maximum Level of Stock is exceeded.')
        return res

