# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def button_quick_preview(self):
        wizard = self.env['sale.order.line.wizard'].create({})
        for line in self.order_line:
            wizard_line = self.env['sale.order.line.wizard.line'].create({
                'wizard_id': wizard.id,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'product_uom_qty': line.product_uom_qty,
            })
        return {
            'name': _('Sale Order Lines'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('aspl_sale_order_quick_preview.view_sale_order_line_wizard_form').id,
            'res_model': 'sale.order.line.wizard',
            'res_id': wizard.id,
            'target': 'new',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
