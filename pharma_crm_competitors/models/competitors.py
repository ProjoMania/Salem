# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CompetitorsImages(models.Model):
    _name = 'competitors.images'
    _description = 'Competitors Images'
    
    image = fields.Image()
    competitor_id = fields.Many2one('competitors')
    
    
class Competitors(models.Model):
    _name = 'competitors'
    _description = 'Competitors'

    name = fields.Char(string="Name", required=True)
    product_id = fields.Many2one(comodel_name='product.product',string="Product", required=True)
    product_price = fields.Float(string="Product Price", required=True)
    image_ids = fields.One2many('competitors.images', 'competitor_id', string="Images")
    
    @api.onchange('product_id')
    def _set_product_price(self):
        if self.product_id:
            self.product_price=self.product_id.lst_price