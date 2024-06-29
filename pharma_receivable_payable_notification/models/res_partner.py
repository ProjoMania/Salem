# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _activity_for_receivable_payable_notification(self):
        activities = []
        activity_type_id = self.env['mail.activity.type'].search([('id', '=', 4)]).id
        partners = self.env['res.partner'].search([])
        for partner in partners:
            if partner.unreconciled_aml_ids:
                for line in partner.unreconciled_aml_ids:
                    if line.date_maturity and (line.date_maturity+timedelta(days=30))<date.today():
                        invoice = partner.env['account.move'].search([('name', '=', line.move_name)])
                        message = "due" if line.amount_residual_currency>0 else "payable"
                        if invoice.invoice_user_id:
                            activity = partner.env['mail.activity'].create({
                                    'res_id': invoice.invoice_user_id.partner_id.id,
                                    'user_id': invoice.invoice_user_id.id,
                                    'res_model_id': partner.env['ir.model']._get_id('res.partner'),
                                    'activity_type_id': activity_type_id,
                                    'summary': f"Please check amount {message} for {line.move_name} with amount {abs(line.amount_residual_currency)} of customer {partner.name}.",
                                    })
                            activity.res_name = line.move_name
                            activities.append(activity)
        return activities
    