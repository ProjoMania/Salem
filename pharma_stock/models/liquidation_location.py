
from odoo import models, fields, api


class Liquidation(models.Model):
    _name = 'liquidation.location'
    _rec_name = 'partner_id'
    _inherit = 'mail.thread'
    _description = "Liquidation Location"

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    location_id = fields.Many2one('stock.location', string="Customer Location")
    liquidation_id = fields.Many2one('stock.location', string="Liquidation Location")
    product_id = fields.Many2one('product.product', string='Product')
    cust_qty = fields.Float(string='Customer Quantity', readonly=True, compute="calculate_qty", default=0)
    liq_qty = fields.Float(string='Liquidation Quantity')
    total_liq_qty = fields.Float(string='Total Liquidation Quantity', readonly=True, compute="calculate_qty", default=0)

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.location_id = self.partner_id.property_stock_customer.id
            self.liquidation_id = self.partner_id.liquidation_id.id

    @api.depends('product_id')
    def calculate_qty(self):
        for rec in self:
            if rec.product_id:
                cust_quant_id = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id),
                                                                ('location_id', '=', rec.location_id.id)])
                liq_quant_id = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id),
                                                               ('location_id', '=', rec.liquidation_id.id)])
                rec.cust_qty = cust_quant_id.quantity
                rec.total_liq_qty = liq_quant_id.quantity
            else:
                rec.cust_qty = 0
                rec.total_liq_qty = 0

    def add_liquidation(self):
        if self.liq_qty:
            picking_vals = {
                'partner_id': self.partner_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.liquidation_id.id,
                'picking_type_id': self.env['stock.picking.type'].search(
                    [('code', '=', 'incoming'), ('company_id', '=', self.env.company.id)], limit=1).id,
                'move_ids_without_package': [
                    (0, 0, {
                        'name': self.partner_id.id,
                        'product_id': self.product_id.id,
                        'product_uom_qty': self.liq_qty,
                        'product_uom': self.product_id.uom_id.id,
                        'location_id': self.location_id.id,
                        'location_dest_id': self.liquidation_id.id,
                    })]
            }
            picking_id = self.env['stock.picking'].create(picking_vals)
            picking_id.action_confirm()
            picking_id.button_validate()
