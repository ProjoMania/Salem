
from odoo import api, fields, models, _

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    workflow_process = fields.Selection(
        [('default', 'Default Workflow'),
         ('workflow_2', 'Workflow 2'),
         ('workflow_3', 'Workflow 3')],
        string='Workflow Process',
        default='default'
    )

class ProductPricelistItem(models.Model):
    _name = "product.pricelist.item"
    _inherit = ['product.pricelist.item', 'analytic.mixin']

    workflow_process = fields.Selection(related='pricelist_id.workflow_process')
    foc_by_vendor = fields.Float(string='FOC by Vendor (%)')
    foc_by_company = fields.Float(string='FOC by Company (%)')
    net_price = fields.Float(string="Net Price")

    analytic_distribution_for_vendor = fields.Json(string="Analytic Distribution for Vendor FOC")
    analytic_distribution_for_company = fields.Json(string="Analytic Distribution for Company FOC")