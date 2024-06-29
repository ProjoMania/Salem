from odoo import models, fields, api, _


class VisitOrder(models.Model):
    _name = "visit.order"
    _rec_name = 'sequence'
    _inherit = ['mail.thread', 'timer.mixin']
    _description = "Visit Order"

    drug_store_id = fields.Many2one('res.partner', string="Drug Store")
    partner_id = fields.Many2one('res.partner', string="Doctor")
    visit_id = fields.Many2one('pharma.visit')
    sequence = fields.Char()
    sales_rep_id = fields.Many2one('res.users', string='Sales Representative', domain=lambda self: [
        ("groups_id", "=", self.env.ref("pharma_sales_rep.group_sales_rep").id)])
    order_date = fields.Date(string="Order Date")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
                                 index=True, required=True)
    status = fields.Selection([('draft', 'Draft'), ('ordered', 'Ordered'),
                               ('waiting_for_drag_store', 'Waiting For Drug Store'),
                               ('delivered', 'Delivered'),
                               ('done', 'Done')], default='draft')
    sale_count = fields.Integer(compute='compute_sale_order_count')
    visit_order_ids = fields.One2many('visit.order.line', 'visit_order_id')

    def compute_sale_order_count(self):
        for visit in self:
            visit.sale_count = self.env['sale.order'].search_count([('visit_id', '=', visit.id)])

    def action_ordered(self):
        self.status = "ordered"

    def action_waiting(self):
        self.status = "waiting_for_drag_store"

    def action_delivered(self):
        self.status = "delivered"

    def action_done(self):
        self.status = "done"
        picking_vals = {
            'partner_id': self.drug_store_id.id,
            'location_id': self.drug_store_id.property_stock_customer.id,
            'location_dest_id': self.drug_store_id.liquidation_id.id,
            'picking_type_id': self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('company_id', '=', self.env.company.id)], limit=1).id,
            'move_ids_without_package': [
                (0, 0, {
                    'name': self.drug_store_id.id,
                    'product_id': each.product_id.id,
                    'product_uom_qty': each.qty,
                    'product_uom': each.product_id.uom_id.id,
                    'location_id': self.drug_store_id.property_stock_customer.id,
                    'location_dest_id': self.drug_store_id.liquidation_id.id,
                }) for each in self.visit_order_ids]
        }
        picking_id = self.env['stock.picking'].create(picking_vals)
        picking_id.action_confirm()
        picking_id.button_validate()

    def action_sale_order(self):
        visit_order_lines = []
        for order in self.visit_order_ids:
            visit_order_lines.append((0, 0, {
                'product_id': order.product_id.id,
                'name': order.product_id.name,
                'price_unit': order.amount,
                'product_uom_qty': order.qty,
                'price_subtotal': order.total,
            }))

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'drug_store_id': self.drug_store_id.id,
            'sales_rep_id': self.sales_rep_id.id,
            'state': 'draft',
            'visit_id': self.id,
            'order_line': visit_order_lines,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': sale_order.id,
            'visit_id': self.id,
            'target': 'current',
        }

    def action_get_sale_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('visit_id', '=', self.id)],
        }

    @api.model
    def create(self, vals):
        sequence_no = self.env['ir.sequence'].next_by_code('visit_order_seq')
        vals.update({'sequence': sequence_no})
        res = super().create(vals)
        return res


class VisitOrderLine(models.Model):
    _name = "visit.order.line"

    visit_order_id = fields.Many2one('visit.order')
    product_id = fields.Many2one('product.product')
    product_category_id = fields.Many2one('product.category', related='product_id.categ_id', readonly=True)
    amount = fields.Float(string='Amount')
    qty = fields.Integer(string='Quantity')
    total = fields.Float(string='Total', readonly=True)
