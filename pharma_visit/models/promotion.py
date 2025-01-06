
from odoo import models, fields, _


class Promotion(models.Model):
    _name = "visit.promotion"
    _description = "Promotion"

    name = fields.Char(string='Promotion Name')
    image_ids = fields.One2many('promotion.images', 'promotion_id', string="Images")


class PromotionImages(models.Model):
    _name = 'promotion.images'
    _description = 'Promotion Images'

    image = fields.Image()
    promotion_id = fields.Many2one('visit.promotion')
