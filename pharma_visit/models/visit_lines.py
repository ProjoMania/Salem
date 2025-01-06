from odoo import models, fields, api, _


class VisitOrders(models.Model):
    _name = "visit.lines"

    visit_id = fields.Many2one('pharma.visit')
    product_id = fields.Many2one('product.product')
    product_category_id = fields.Many2one('product.category', related='product_id.categ_id')
    amount = fields.Float(string='Amount')
    qty = fields.Integer(string='Quantity')
    total = fields.Float(string='Total', store=True, readonly=True, compute="compute_total")
    drug_store_id = fields.Many2one('res.partner', string="Drug Store")
    avail_qty = fields.Float(string='Available Qty', readonly=True, compute="compute_qty")
    company_id = fields.Many2one(related="visit_id.company_id")

    def default_currency_id(self):
        return self.env.user.company_id.currency_id.symbol

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.amount = self.product_id.lst_price

    @api.depends('drug_store_id')
    def compute_qty(self):
        for rec in self:
            if rec.product_id:
                if rec.drug_store_id:
                    location_id = rec.drug_store_id.property_stock_customer
                    quants = self.env['stock.quant'].search(
                        [('location_id', '=', location_id.id), ('product_id', '=', rec.product_id.id)])
                    available_quantity = sum(quant.quantity for quant in quants)
                    rec.avail_qty = available_quantity
                else:
                    rec.avail_qty = 0
            else:
                rec.avail_qty = 0

    @api.depends('amount', 'qty')
    def compute_total(self):
        for each in self:
            each.total = each.amount * each.qty

    def add_foc_product_product(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Add Product',
            'res_model': 'foc.product',
            'view_mode': 'tree',
            'domain': [('product_id.product_variant_id.id', '=', self.product_id.id)],
            'target': 'new',
        }
        return action
