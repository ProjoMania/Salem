# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from odoo.http import request


class HrJob(models.Model):
    _inherit = 'hr.job'

    survey_id = fields.Many2one('survey.survey', string='Survey')

    @api.model
    def get_survey_id(self, job_id):
        return self.sudo().browse(job_id).survey_id


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    result_ids = fields.One2many('survey.user_input', 'applicant_id', string='Results')
    survey_result_count=fields.Integer(compute='_compute_survey_result_count')

    @api.depends('result_ids')
    def _compute_survey_result_count(self):
        for rec in self:
            rec.survey_result_count=len(rec.result_ids)
    def action_open_survey_result(self):
        self.ensure_one()
        return {
            'name': _('Survey Results'),
            'type': 'ir.actions.act_window',
            'res_model': 'survey.user_input',
            'view_mode': 'list,form',
            'domain': [('applicant_id', '=', self.id)],
            'context': {'default_applicant_id': self.id},
        }



class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')

    @api.model
    def create(self, vals):
        res = super(SurveyUserInput, self).create(vals)
        applicant_id=self.env['hr.applicant'].sudo().browse(request.session.get('REQ').get('applicant_id'))
        if applicant_id:
            res.email=applicant_id.email_from
            res.applicant_id=applicant_id.id
        return res
