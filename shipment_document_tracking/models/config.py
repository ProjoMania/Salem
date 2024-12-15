from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_shipment_tracking = fields.Boolean("Allow Shipment Tracking", related="company_id.allow_shipment_tracking",
                                             readonly=False)


class Company(models.Model):
    _inherit = 'res.company'

    allow_shipment_tracking = fields.Boolean(string='Allow Shipment Tracking', default=False,
        help='Allows tracking of shipments')