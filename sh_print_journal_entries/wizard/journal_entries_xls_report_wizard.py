# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import xlwt
import base64
from io import BytesIO
import html2text


class JournalEntriesDetailExcelExtended(models.Model):
    _name = "journal.entries.detail.excel.extended"
    _description = 'Excel Entries Extended'

    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)

    def download_report(self):

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=journal.entries.detail.excel.extended&field=excel_file&download=true&id=%s&filename=%s' % (self.id, self.file_name),
            'target': 'new',
        }


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_entries_xls_entry(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'sh_print_journal_entries.sh_journal_entries_details_report_wizard_form_action')
        # Force the values of the move line in the context to avoid issues
        ctx = dict(self.env.context)
        ctx.pop('active_id', None)
        ctx['active_ids'] = self.ids
        ctx['active_model'] = 'account.move'
        action['context'] = ctx
        return action


class ShJournalEntriesDetailsReportWizard(models.TransientModel):
    _name = "sh.journal.entries.details.report.wizard"
    _description = 'Journal Entries details report wizard model'

    def print_journal_entries_xls_report(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;borders:top thick;borders:bottom thick;')
        bold = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        border = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour gray25;borders:top thick;borders:bottom thick;')
        format1 = xlwt.easyxf('font:bold True;;align: horiz left')

        data = {}
        data = dict(data or {})
        active_ids = self.env.context.get('active_ids')

        account_move = self.env['account.move'].search(
            [('id', 'in', active_ids)])
        
        handle = html2text.HTML2Text()
        for move in account_move:
            journal_lines = []
            final_value = {}
            count = 0

            final_value['journal_name'] = move.name
            final_value['ref'] = move.ref
            final_value['date'] = move.date
            final_value['journal_id'] = move.journal_id.name
            final_value['narration'] = ''
            if move.narration :
                final_value['narration'] = handle.handle(move.narration)

            for lines in move.line_ids:
                count += 1
                product = {
                    'count': count,
                    'account_id': lines.account_id,
                    'partner_id': lines.partner_id,
                    'name': lines.name,
                    'analytic_account_id': lines.analytic_account_id,
                    'debit': lines.debit,
                    'credit': lines.credit,
                    'date_maturity': lines.date_maturity,
                }
                journal_lines.append(product)

            if move.name == '/':
                worksheet = workbook.add_sheet("Draft", cell_overwrite_ok=True)
            else:
                worksheet = workbook.add_sheet(
                    move.name, cell_overwrite_ok=True)

            worksheet.write_merge(
                0, 1, 0, 7, 'Journal Entries Details', heading_format)

            worksheet.col(0).width = int(5 * 260)
            worksheet.col(1).width = int(22 * 260)
            worksheet.col(2).width = int(18 * 260)
            worksheet.col(3).width = int(50 * 260)
            worksheet.col(4).width = int(20 * 260)
            worksheet.col(5).width = int(18 * 260)
            worksheet.col(6).width = int(18 * 260)
            worksheet.col(7).width = int(13 * 260)

            worksheet.write(3, 1, "Journal Entry #", format1)
            worksheet.write(3, 2, final_value['journal_name'])
            worksheet.write(3, 4, "Reference", format1)
            if final_value['ref']:
                worksheet.write(3, 5, final_value['ref'])

            worksheet.write(4, 1, "Date", format1)
            worksheet.write(4, 2, str(final_value['date']))
            worksheet.write(4, 4, "Journal", format1)
            worksheet.write(4, 5, final_value['journal_id'])

            worksheet.write(7, 0, "Sr", bold)
            worksheet.write(7, 1, "Account", bold)
            worksheet.write(7, 2, "Partner", bold)
            worksheet.write(7, 3, "Label", bold)
            worksheet.write(7, 4, "Analytic Account", bold)
            worksheet.write(7, 5, "Debit", bold)
            worksheet.write(7, 6, "Credit", bold)
            worksheet.write(7, 7, "Due Date", bold)

            row = 8
            total_debit = 0.0
            total_credit = 0.0

            for rec in journal_lines:

                if rec.get('count'):
                    worksheet.write(row, 0, rec.get('count'))
                if rec.get('account_id'):
                    worksheet.write(row, 1, str(rec.get('account_id').name))
                if rec.get('partner_id'):
                    worksheet.write(row, 2, str(rec.get('partner_id').name))
                if rec.get('name'):
                    worksheet.write(row, 3, str(rec.get('name')))
                if rec.get('analytic_account_id'):
                    worksheet.write(row, 4, rec.get('analytic_account_id'))
                if rec.get('debit'):
                    worksheet.write(row, 5, rec.get('debit'))
                if rec.get('credit'):
                    worksheet.write(row, 6, rec.get('credit'))
                if rec.get('date_maturity'):
                    worksheet.write(row, 7, str(rec.get('date_maturity')))

                total_debit += rec.get('debit')

                total_credit += rec.get('credit')

                row += 1

            row += 1
            worksheet.write(row, 0, '', border)
            worksheet.write(row, 1, "Total", border)
            worksheet.write_merge(row, row, 2, 4, '', border)
            worksheet.write(row, 5, total_debit, border)
            worksheet.write(row, 6, total_credit, border)
            worksheet.write(row, 7, '', border)

            row += 2
            if final_value['narration']:
                worksheet.write(row, 0, '')
                worksheet.write(row, 1, "Internal Note :", format1)
                row += 1
                worksheet.write_merge(
                    row, row+5, 1, 3, final_value['narration'])

        filename = ('Journal Entries Detail Xls Report' + '.xls')
        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['journal.entries.detail.excel.extended'].sudo().create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename,
        })

        return{
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=journal.entries.detail.excel.extended&field=excel_file&download=true&id=%s&filename=%s' % (export_id.id, export_id.file_name),
            'target': 'new',
        }
