from odoo import api, models, fields, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    tracking_id = fields.Many2one('shipment.doc.tracking', 'Tracking Order')
    tracking_status = fields.Selection(related="tracking_id.status")

    def view_shipment_tracking(self):
        return {
            'name': _('Tracking Order'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.tracking_id.id,
            'res_model': self.tracking_id._name
        }