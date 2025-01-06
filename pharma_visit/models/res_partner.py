from odoo import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    visit_classification_id = fields.Many2one('doctor.classification', string='Doctor Classification')
    speciality_id = fields.Many2one('doctor.speciality', string='Speciality')
    sub_speciality_id = fields.Many2one('doctor.sub_speciality', string='Sub Speciality')
    brik_id = fields.Many2one('briks.briks', string='Briks')
    is_type = fields.Boolean(compute='_compute_type')

    @api.depends('customer_type')
    def _compute_type(self):
        type_id = self.env.ref('pharma_visit.type_doctor').id
        for partner in self:
            partner.is_type = (partner.customer_type.id == type_id)
