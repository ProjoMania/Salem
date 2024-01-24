# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

from datetime import datetime



class ChangeAccount(models.TransientModel):
    _name = 'partner.print.wizard'
    _description = 'Partner Print Wizard'

    partner_id = fields.Many2one('res.partner', 'Partner')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')

    # property_account_receivable_id
    # property_account_payable_id

    def view_statement(self):
        partner = self.partner_id
        account_id = partner.property_account_receivable_id and partner.property_account_receivable_id.id
        if not account_id:
            raise UserError(
                _('Account Is not found for %s !', partner.name))
        date = self.date_from
        date_to = self.date_to if self.date_to else  datetime.today().date()
        line_ids = []
        payment_lines = []
        statement_dict = {
            'name': 'Customer Statement as On '+ str(date),
            'partner_id':self.partner_id.id,
            'date': self.date_from,
            'date_to': self.date_to,
        }
        sales_domain = [('partner_id','=',partner.id),('state','in',('sale','done')),('date_order','>=',date)]
        payment_domain = [('partner_id','=',partner.id),('state','=','posted'),
                                        ('payment_type','=','inbound'),('payment_date','>=',date)]
        if self.date_to:
            sales_domain.append(('date_order','<=',self.date_to))
            payment_domain.append(('payment_date','<=',self.date_to))


        self.env.cr.execute("select sum(debit)-sum(credit) as balance from account_move_line where partner_id = %s and date < %s and account_id = %s",
                    (partner.id, date,account_id))


        initial = self.env.cr.fetchone()
        initial_bal = initial and initial[0] or 0.0
        self.env.cr.execute("select sum(debit)-sum(credit) as balance from account_move_line where partner_id = %s and account_id = %s",
                            (partner.id,account_id,),)
        balance = self.env.cr.fetchone()
        balance = balance and balance[0] or 0.0
        sales = self.env['sale.order'].search(sales_domain)
        so_total = 0
        payments = self.env['account.payment'].search(payment_domain)
        # payment_total = sum(payments.mapped('amount'))
        payment_total = 0.0

        statement_dict['inital_total'] = initial_bal

        statement_dict['balance'] = balance

        for order in sales:
            total = order.amount_total / order.currency_rate
            payment_status = order.mapped
            invoices = order.invoice_ids.filtered(lambda invoice: invoice.state == 'posted')
            payment_status = 'Not Paid'
            if invoices:
                print (invoices[0].payment_state,dict(invoices[0]._fields['payment_state'].selection))
                payment_status = dict(invoices[0]._fields['payment_state'].selection).get(invoices[0].payment_state)
                print ("status",payment_status)
            so_total += total
            line_ids.append((0, 0, {
                    'order_id': order.id,
                    'date': order.date_order.strftime('%Y-%m-%d'),
                    'currency_id': order.currency_id and order.currency_id.id or False,
                    'amount': total,
                    'amount_currency': order.amount_total,
                    'payment_status': payment_status,
            }))

        for payment in payments:
            total = sum(payment.move_id.line_ids.mapped('debit'))
            payment_total += total
            invoices = ''.join([inv.name for inv in payment.reconciled_invoice_ids])
            so = self.env['sale.order'].search([('invoice_ids','in',payment.reconciled_invoice_ids.ids)])
            order_ref = ''.join([s.name for s in so])
            payment_lines.append((0,0, {
                'acc_payment_id': payment.id,
                'date': payment.date,
                'amount_currency': payment.amount,
                'currency_id': payment.currency_id and payment.currency_id.id or False,
                'amount': total,
                'invoice_ref': invoices,
                'order_ref': order_ref
            }))
        statement_dict['so_total'] = so_total
        statement_dict['payment_total'] = payment_total
        statement_dict['order_lines'] = line_ids
        statement_dict['payment_lines'] = payment_lines
        self.env['account.partner.statement'].search([]).unlink()
        statement = self.env['account.partner.statement'].create(statement_dict)

        return {
            'name': "Partner Statement",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.partner.statement',
            'res_id': statement.id,
        }

