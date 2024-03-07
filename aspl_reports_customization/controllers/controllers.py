from odoo import http
from odoo.http import request
from odoo.http import content_disposition
from odoo import SUPERUSER_ID


class WebsiteProductDetails(http.Controller):

    @http.route(['/check_name_in_database'], type='http', auth="public", website=True, sitemap=True)
    def products_details(self, model=None):
        name = model.split('?')
        name1 = request.env[name[0]].sudo().search([('id', '=', name[1])])
        if name1:
            return http.request.render("aspl_reports_customization.website_valid_doc_template",
                                       {'id': name1, 'model': name[0], 'record': name1})
        else:
            return http.request.render("aspl_reports_customization.website_invalid_doc_template")

    @http.route(['/print_document'], type='http', auth="public", website=True, csrf=False)
    def print_document(self, **kwargs):
        model = kwargs.get('model_name')
        doc_id = request.env[model].sudo().search([('id', '=', kwargs.get('doc_id'))])
        # doc_id = kwargs.get('record_id')
        if model == 'sale.order':
            report_name = 'sale.report_saleorder'
        elif model == 'account.move':
            report_name = 'account.report_invoice_with_payments'
        elif model == 'purchase.order':
            report_name = 'purchase.report_purchaseorder'
        elif model == 'hr.expense.sheet':
            report_name = 'hr_expense.report_expense_sheet'
        elif model == 'hr.payslip':
            report_name = 'hr_payroll.report_payslip_lang'
        elif model == 'stock.picking':
            # if doc_id.name == 'outgoing':
            report_name = 'stock.report_deliveryslip'
            # else:
            #     report_name = 'stock.report_picking'

        pdf, _ = request.env['ir.actions.report']._get_report_from_name(
            report_name).with_user(SUPERUSER_ID).sudo()._render_qweb_pdf([int(doc_id.sudo().id)])
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', content_disposition('Report-%s.pdf' % (doc_id.name)))
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route(['/picking/pdf/<int:picking_id>'], type='http', auth="public", website=True, sitemap=True)
    def picking_pdf(self, picking_id):
        pdf = \
        request.env.ref('stock.action_report_delivery').with_user(SUPERUSER_ID)._render_qweb_pdf([picking_id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)