from odoo import models, api, fields

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    partner_category_id = fields.Many2many(related='partner_id.category_id',string='Tags',readonly=False)