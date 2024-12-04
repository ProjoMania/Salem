
from odoo.addons.website.controllers import form
from odoo.http import request
from odoo import http
import json

class WebsiteForm(form.WebsiteForm):

    def website_form(self, model_name, **kwargs):
        if model_name == 'hr.applicant':
            survey_id = request.env['hr.job'].sudo().get_survey_id(int(kwargs.get('job_id')))
            job_id = request.env['hr.job'].sudo().browse(int(kwargs.get('job_id')))
            if survey_id :
                url=survey_id.sudo().get_start_url()
                res=super(WebsiteForm, self).website_form(model_name, **kwargs)
                applicant_id=json.loads(res.data.decode('utf-8')).get('id',0)
                vals={'survey_url': url, 'applicant_id': applicant_id, 'job': job_id.id}
                request.session['REQ'] = vals
                return res
        return super(WebsiteForm, self).website_form(model_name, **kwargs)

    @http.route('/apply/success', type='http', auth="public", methods=['GET'], website=True, csrf=False)
    def apply_success(self,**kwargs):
        return request.redirect(request.session['REQ']['survey_url'])
