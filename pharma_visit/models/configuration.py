from odoo import models, fields, api, _


class DealTrack(models.Model):
    _name = "deal.track"
    _rec_name = "deal_id"

    deal_id = fields.Many2one('visit.deal', string="Deal")
    consumed_qty = fields.Integer(string="Consumed Quantity")
    date = fields.Date(string="Date")
    comments = fields.Text(string="Comments")


class VisitDeal(models.Model):
    _name = "visit.deal"
    _rec_name = "competitor_id"

    competitor_id = fields.Many2one('competitors', string="Competitors")
    qty = fields.Integer(string="Quantity")
    start_date = fields.Date(string="Start Date")
    Expected_expiry_date = fields.Date(string="Expected Expiry Date")
    comments = fields.Text(string="Comments")


class PromoPapers(models.Model):
    _name = "promo.papers"
    _rec_name = "name"

    name = fields.Char(string="Name")
    file = fields.Binary(string="File")
    product_id = fields.Many2one('product.product', string="Product")


class MedicalPaper(models.Model):
    _name = "medical.paper"
    _rec_name = "name"

    name = fields.Char(string="Name")
    file = fields.Binary(string="File")
    product_id = fields.Many2one('product.product', string="Product")
