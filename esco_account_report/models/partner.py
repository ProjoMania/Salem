# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter
import json
from odoo.tools import date_utils
import io
from datetime import datetime

class PartnerStatement(models.Model):
    _name = "account.partner.statement"
    _description = 'Partner Statement'

    def _get_currency(self):
        return self.env.user.company_id.currency_id

    def _get_company(self):
        return self.env.user.company_id


    name = fields.Char('Report Name')
    date = fields.Date('Date')
    date_to = fields.Date('Date To')
    partner_id = fields.Many2one('res.partner','Partner')
    inital_total = fields.Monetary("Initial Total")
    so_total = fields.Monetary("SO Total")
    currency_id = fields.Many2one('res.currency', default=_get_currency)
    company_id = fields.Many2one('res.company', default=_get_company)
    payment_total = fields.Monetary("Payment Total")
    balance = fields.Monetary("Balance")
    order_lines = fields.One2many('partner.detail.lines','statement_id')
    payment_lines = fields.One2many('partner.detail.lines','payment_id')

    def action_print_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
        }
        report_name = 'Customer Statement'
        print ("data========",data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'account.partner.statement',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'report.esco_account_report.report_customer_statement_xlsx',
                     'reportname': 'esco_account_report.report_customer_statement_xlsx',
                     },
            'report_type': 'xlsx'
        }


class CustomerStatement(models.AbstractModel):
    _name = 'report.esco_account_report.report_customer_statement_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Customer Statement Report'

    def generate_xlsx_report(self, workbook, data, vendors):
        report = self.env['account.partner.statement'].search([], limit=1)
        header_bold_style = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'bg_color': '#8f9194', 'font_size': 16})
        header_bold_style.set_align('center')
        header_bold_style1 = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'bg_color': '#8f9194', 'font_size': 10,'align':'center'})
        header_bold_style_number = workbook.add_format(
            {'bold': True, 'bg_color': '#8f9194', 'font_size': 14, 'num_format': '$#,##0.00'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'yyyy-mm-dd'})
        datetime_style = workbook.add_format({'text_wrap': True, 'num_format': 'yyyy-mm-dd hh:mm:ss'})

        format1 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': False})
        format2.set_align('right')
        font_size_9 = workbook.add_format({'font_size': 9, 'align': 'left'})
        currency_format = workbook.add_format({'num_format': report.currency_id.symbol+'#,##0.00'})
        currency_format_bold = workbook.add_format({'num_format': report.currency_id.symbol+'#,##0.00', 'bold': True})
        sheet = workbook.add_worksheet('Customer Statement')

        sheet.set_column(0, 0, 7)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 17)
        sheet.set_column(3, 3, 7)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 17)
        header_name = 'Customer Statement As on ' + str(datetime.today().date())
        sheet.merge_range('A1:F1', header_name, header_bold_style)
        sheet.write(1, 1, 'Start Date:', format1)
        sheet.write(1, 2, str(report.date), format1)
        sheet.write(1, 4, 'End Date:', format1)
        sheet.write(1, 5, str(report.date_to or ''), format1)

        sheet.merge_range('C3:E3', "Customer: "+report.partner_id.name, header_bold_style1)
        row = 3
        sheet.write(row, 1, 'Initial Balance:', format1)
        sheet.write(row, 2, report.inital_total, currency_format_bold)
        sheet.write(row, 4, 'Total Orders:', format1)
        sheet.write(row, 5, report.so_total, currency_format_bold)

        sheet.write(row+1, 1, 'Total Payments:', format1)
        sheet.write(row+1, 2, report.payment_total, currency_format_bold)
        sheet.write(row+1, 4, 'Total Balance:', format1)
        sheet.write(row+1, 5, report.balance, currency_format_bold)
        row = 6
        sheet.merge_range('B6:F6', "Order Details", header_bold_style1)

        sheet.write(row , 1, 'Order#', format1)
        sheet.write(row, 2, 'Date#', format1)
        sheet.write(row, 3, 'Amount In Currency', format1)
        sheet.write(row, 4, 'Amount', format1)
        row += 1
        for order in report.order_lines:
            new_currency = workbook.add_format({'num_format': order.currency_id.symbol + '#,##0.00'})
            sheet.write(row, 1, order.order_id.name, font_size_9)
            sheet.write(row, 2, str(order.date), font_size_9)
            sheet.write(row, 3, order.amount_currency, new_currency)
            sheet.write(row, 4, order.amount, currency_format)
            row += 1

        row = row+1
        col1 = 'B'+str(row) + ':' + 'F'+ str(row)
        sheet.merge_range(col1, "Payment Details", header_bold_style1)
        sheet.write(row, 1, 'Payment No#', format1)
        sheet.write(row, 2, 'Date#', format1)
        sheet.write(row, 3, 'Amount In Currency', format1)
        sheet.write(row, 4, 'Amount', format1)
        row += 1
        for payment in report.payment_lines:
            new_currency = workbook.add_format({'num_format': payment.currency_id.symbol + '#,##0.00'})
            sheet.write(row, 1, payment.acc_payment_id.name, font_size_9)
            sheet.write(row, 2, str(payment.date), font_size_9)
            sheet.write(row, 3, payment.amount_currency, new_currency)
            sheet.write(row, 4, payment.amount, currency_format)
            row += 1



    def get_xlsx_report(self, data, response):
        output = io.BytesIO()

        report = self.search([('id', 'in', data.get('ids', []))], limit=1)
        self.env.cr.execute("select id,code from account_account")
        acc_data = self.env.cr.fetchall()
        accs = dict(acc_data)

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        report_name = 'Balance Sheet'
        if report.is_pl:
            report_name='PL Statement'
        sheet = workbook.add_worksheet(report_name)

        base_style = workbook.add_format({'text_wrap': True})
        header_style = workbook.add_format({'bold': True})
        header_bold_style = workbook.add_format({'text_wrap': True, 'bold': True, 'bg_color': '#8f9194','font_size': 16})

        header_bold_style.set_align('center')
        header_bold_style_number = workbook.add_format(
            {'bold': True, 'bg_color': '#8f9194', 'font_size': 14,'num_format': '$#,##0.00'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'yyyy-mm-dd'})
        datetime_style = workbook.add_format({'text_wrap': True, 'num_format': 'yyyy-mm-dd hh:mm:ss'})

        format1 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': False})
        format2.set_align('right')
        font_size_8 = workbook.add_format({'font_size': 9, 'align': 'left'})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})
        currency_format_bold = workbook.add_format({'num_format': '$#,##0.00','bold': True})


        sheet.set_column(0, 0, 7)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 17)
        sheet.set_column(3, 3, 7)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 17)
        # sheet.write(2, 0, 'Liabilities', format1)
        header_name = 'Customer Statement As on '+ str(report.date_to)
        sheet.merge_range('C1:F1', header_name, header_bold_style)


        # sheet.write(2, 1, 'Balance', format1)


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



class Details(models.Model):
    _name = 'partner.detail.lines'
    _description = "Partner Details"


    def _get_currency(self):
        return self.env.user.company_id.currency_id

    statement_id = fields.Many2one('account.partner.statement', 'Statement')
    payment_id = fields.Many2one('account.partner.statement', 'Payments')
    acc_payment_id = fields.Many2one('account.payment', 'Payment')
    order_ref = fields.Char("Order Ref")
    order_id = fields.Many2one("sale.order", string='Order#')
    date = fields.Date('Date')
    company_currency_id = fields.Many2one('res.currency',string='Base Currency', default=_get_currency)
    currency_id = fields.Many2one('res.currency','Currency')
    amount_currency = fields.Monetary('Amount In Currency', currency_field='currency_id')
    amount = fields.Monetary('Amount', currency_field='company_currency_id')
    payment_status = fields.Char("Payment Status")
    invoice_ref = fields.Char("Invoices")
