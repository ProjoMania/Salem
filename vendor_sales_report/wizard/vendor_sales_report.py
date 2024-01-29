# -*- encoding: utf-8 -*-
import io
import base64
import xlwt
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VendorSalesReport(models.TransientModel):
    _name = 'vendor.sales.report'

    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    from_date = fields.Date(string="From date", tracking=True, required=True)
    to_date = fields.Date(string="To date", tracking=True, required=True)

    def print_report_xls_menu(self):
        partner = self.vendor_id
        filename = 'Vendor Sales Report' + '.xls'
        res_company = self.env.company
        vendor_data_list = []
        suppliers_for_mail = self.env['product.supplierinfo'].sudo().search([("name", "=", partner.id)])

        if suppliers_for_mail:
            product_list = []
            for supplier in suppliers_for_mail:
                product = supplier.product_tmpl_id
                product_product = self.env['product.product'].sudo().search([("product_tmpl_id", "=", product.id)])
                product_list.append(product_product.ids)
            import itertools
            products_list = list(itertools.chain.from_iterable(product_list))
            stock_lines = self.env['stock.move.line'].sudo().search([("product_id", "in", products_list)])

            if stock_lines:
                lots_obj = self.env["stock.lot"].search([])
                # sale_orders = self.env["sale.order"].search([("date_order", ">=", from_dt), ("date_order", "<=", to_dt),
                #                                              ("name", "=", 'BDI-SO-2022-0424')])
                                                             # ("name", "in", ('BDI-SO-2022-1302','BDI-SO-2022-0134','BDI-SO-2022-0007'))])
                sale_orders = self.env["sale.order"].search([])
                ############################################################################################################
                # move type = out_invoice
                ############################################################################################################
                for invoice in sale_orders.invoice_ids.invoice_line_ids.filtered(lambda o: o.product_id.id in products_list and o.move_id.move_type == 'out_invoice' and o.move_id.invoice_date >= self.from_date and o.move_id.invoice_date <= self.to_date and o.move_id.state != 'cancel'):
                    lot_str = False
                    total_qty = 0
                    # this code for select the lot from Delivery according to the same quantity
                    for line in invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(lambda o: o.picking_id.backorder_id.id == False and o.picking_id.picking_type_code == 'outgoing' and o.picking_id.state == 'done'):
                        if line.qty_done == invoice.quantity and line.product_id == invoice.product_id:
                            lot_str = line.lot_id.name
                            break
                        else:
                            continue
                    # This code to select lot where the previous code dose not matched
                    # multi delivery line with multi lot
                    if not lot_str:
                        lot_str = False
                        total_qty = 0
                        for picking in invoice.sale_line_ids.order_id.picking_ids.filtered(lambda o: o.backorder_id.id == False and o.picking_type_code == 'outgoing' and o.state == 'done'):
                            total_qty = 0
                            for line in picking.move_line_ids_without_package:
                                if line.product_id == invoice.product_id:
                                    lot_ids = invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                                        lambda o: o.product_id == invoice.product_id and o.picking_id.id == line.picking_id.id).mapped('lot_id')
                                    if lot_ids:
                                        lots = lots_obj.search([("id", "in", lot_ids.ids)])
                                        lot_str = ''
                                        for lot in lots:
                                            lot_str += str(lot.name) + ', '
                                # if line.product_id == invoice.product_id:
                                #     total_qty += line.qty_done
                                #     if total_qty == invoice.quantity:
                                #         total_qty = 0
                                #         lot_ids = invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                                #             lambda o: o.product_id == invoice.product_id and o.picking_id.id == line.picking_id.id).mapped('lot_id')
                                #         if lot_ids:
                                #             lots = lots_obj.search([("id", "in", lot_ids.ids)])
                                #             lot_str = ''
                                #             for lot in lots:
                                #                 lot_str += str(lot.name) + ', '

                    if invoice:
                        vendor_based_data = {
                            "lot":  lot_str if lot_str else "",
                            "vendor": partner.name if partner else "",
                            "invoice": invoice.move_id.name if invoice else "",
                            "sale_order": invoice.sale_line_ids.order_id.name if invoice.sale_line_ids.order_id.name else "",
                            "invoice_date": invoice.move_id.invoice_date if invoice else "",
                            "default_code": invoice.product_id.default_code if invoice.product_id.default_code else "",
                            "product_name": invoice.product_id.name if invoice.product_id.name else "",
                            "team_id": invoice.move_id.team_id.name if invoice.move_id.team_id.name else "",
                            "area": invoice.move_id.partner_id.area if invoice.move_id.partner_id.area else "",
                            "province": invoice.move_id.partner_id.state_id.name if invoice.move_id.partner_id.state_id.name else "",
                            "district": invoice.move_id.partner_id.street if invoice.move_id.partner_id.street else "",
                            "price_unit": invoice.price_unit if invoice.price_unit else "",
                            "customer_name": invoice.move_id.partner_id.name if invoice.move_id.partner_id.name else "",
                            "quantity": invoice.quantity if invoice.quantity else "0",
                            "price_subtotal": invoice.price_subtotal if invoice.price_subtotal else "0",
                            "currency": invoice.currency_id.name if invoice.currency_id.name else "",
                            "invoice_type": "Invoice",
                        }
                        vendor_data_list.append(vendor_based_data)
                ############################################################################################################
                # move type = credit notes(out_refund)
                ############################################################################################################
                for invoice in sale_orders.invoice_ids.invoice_line_ids.filtered(lambda o: o.product_id.id in products_list and o.move_id.move_type == 'out_refund' and o.move_id.invoice_date >= self.from_date and o.move_id.invoice_date <= self.to_date and o.move_id.state != 'cancel'):
                    lot_str = False
                    # this code for select the lot from Delivery according to the same quantity
                    for line in invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(lambda o: o.picking_id.picking_type_code == 'incoming' and o.picking_id.state == 'done'):
                        if line.qty_done == invoice.quantity and line.product_id == invoice.product_id:
                            lot_str = line.lot_id.name
                            break
                        else:
                            continue
                    # This code to select lot where the breviouse code dose not matched
                    # multi delivery line with multi lot
                    if not lot_str:
                        lot_str = False
                        total_qty = 0
                        for picking in invoice.sale_line_ids.order_id.picking_ids.filtered(lambda o: o.picking_type_code == 'incoming' and o.state == 'done'):
                            total_qty = 0
                            for line in picking.move_line_ids_without_package:
                                if line.product_id == invoice.product_id:
                                    lot_ids = invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                                        lambda o: o.product_id == invoice.product_id and o.picking_id.id == line.picking_id.id).mapped('lot_id')
                                    if lot_ids:
                                        lots = lots_obj.search([("id", "in", lot_ids.ids)])
                                        lot_str = ''
                                        for lot in lots:
                                            lot_str += str(lot.name) + ', '
                                # if line.product_id == invoice.product_id:
                                #     total_qty += line.qty_done
                                #     if total_qty == invoice.quantity:
                                #         total_qty = 0
                                #         lot_ids = invoice.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                                #             lambda o: o.product_id == invoice.product_id and o.picking_id.id == line.picking_id.id).mapped('lot_id')
                                #         if lot_ids:
                                #             lots = lots_obj.search([("id", "in", lot_ids.ids)])
                                #             lot_str = ''
                                #             for lot in lots:
                                #                 lot_str += str(lot.name) + ', '

                    if invoice:
                        vendor_based_data = {
                            "lot":  lot_str if lot_str else "",
                            "vendor": partner.name if partner else "",
                            "invoice": invoice.move_id.name if invoice else "",
                            "sale_order": invoice.sale_line_ids.order_id.name if invoice.sale_line_ids.order_id.name else "",
                            "invoice_date": invoice.move_id.invoice_date if invoice else "",
                            "default_code": invoice.product_id.default_code if invoice.product_id.default_code else "",
                            "product_name": invoice.product_id.name if invoice.product_id.name else "",
                            "team_id": invoice.move_id.team_id.name if invoice.move_id.team_id.name else "",
                            "area": invoice.move_id.partner_id.area if invoice.move_id.partner_id.area else "",
                            "province": invoice.move_id.partner_id.state_id.name if invoice.move_id.partner_id.state_id.name else "",
                            "district": invoice.move_id.partner_id.street if invoice.move_id.partner_id.street else "",
                            "price_unit": invoice.price_unit if invoice.price_unit else "",
                            "customer_name": invoice.move_id.partner_id.name if invoice.move_id.partner_id.name else "",
                            "quantity": -1 * invoice.quantity if invoice.quantity else "0",
                            "price_subtotal": -1 * invoice.price_subtotal if invoice.price_subtotal else "0",
                            "currency": invoice.currency_id.name if invoice.currency_id.name else "",
                            "invoice_type": "Credit Note",
                        }
                        vendor_data_list.append(vendor_based_data)
        data = {
            "company": res_company.name,
            "vendor_based": vendor_data_list,
            "start_date": self.from_date,
            "end_date": self.to_date
        }
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Vendor Sales Report')
        head_style = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour Tan;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
        style1 = xlwt.easyxf('font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz center;')

        if data['vendor_based']:
            worksheet.write(1, 0, 'Start Date', head_style)
            worksheet.write(1, 1, str(data['start_date']), style1)
            worksheet.write(2, 0, 'End Date', head_style)
            worksheet.write(2, 1, str(data['end_date']), style1)
            worksheet.write(3, 0, 'Vendor', head_style)
            worksheet.write(3, 1, 'Item Number', head_style)
            worksheet.write(3, 2, 'Item Name', head_style)
            worksheet.write(3, 3, 'Batch/ Lot', head_style)
            worksheet.write(3, 4, 'Office', head_style)
            worksheet.write(3, 5, 'Area', head_style)
            worksheet.write(3, 6, 'Province', head_style)
            worksheet.write(3, 7, 'District', head_style)
            worksheet.write(3, 8, 'Customer', head_style)
            worksheet.write(3, 9, 'Quantity', head_style)
            worksheet.write(3, 10, 'Sale Order #', head_style)
            worksheet.write(3, 11, 'Invoice #', head_style)
            worksheet.write(3, 12, 'Invoice Date', head_style)
            worksheet.write(3, 13, 'Unit Price', head_style)
            worksheet.write(3, 14, 'Total Amount', head_style)
            worksheet.write(3, 15, 'Currency', head_style)
            worksheet.write(3, 16, 'Type', head_style)
            worksheet.col(0).width = 5000
            worksheet.col(1).width = 5000
            worksheet.col(2).width = 10000
            worksheet.col(3).width = 5000
            worksheet.col(4).width = 5000
            worksheet.col(5).width = 5000
            worksheet.col(6).width = 7000
            worksheet.col(7).width = 7000
            worksheet.col(8).width = 10000
            worksheet.col(9).width = 5000
            worksheet.col(10).width = 7000
            worksheet.col(11).width = 7000
            worksheet.col(12).width = 5000
            worksheet.col(13).width = 5000
            worksheet.col(14).width = 5000
            worksheet.col(15).width = 5000
            worksheet.col(16).width = 5000
            worksheet.row(3).height = 400

            row = 4
            col = 0

            for c in data['vendor_based']:
                if c['invoice'] and c['vendor']:
                    worksheet.write(row, col + 0, str(c['vendor']), style1)
                    worksheet.write(row, col + 1, str(c['default_code']), style1)
                    worksheet.write(row, col + 2, str(c['product_name']), style1)
                    worksheet.write(row, col + 3, str(c['lot']), style1)
                    worksheet.write(row, col + 4, str(c['team_id']), style1)
                    worksheet.write(row, col + 5, str(c['area']), style1)
                    worksheet.write(row, col + 6, str(c['province']), style1)
                    worksheet.write(row, col + 7, str(c['district']), style1)
                    worksheet.write(row, col + 8, str(c['customer_name']), style1)
                    worksheet.write(row, col + 9, str(c['quantity']), style1)
                    worksheet.write(row, col + 10, str(c['sale_order']), style1)
                    worksheet.write(row, col + 11, str(c['invoice']), style1)
                    worksheet.write(row, col + 12, str(c['invoice_date']), style1)
                    worksheet.write(row, col + 13, str(c['price_unit']), style1)
                    worksheet.write(row, col + 14, str(c['price_subtotal']), style1)
                    worksheet.write(row, col + 15, str(c['currency']), style1)
                    worksheet.write(row, col + 16, str(c['invoice_type']), style1)
                    row += 1
            fp = io.BytesIO()
            workbook.save(fp)
            report_id = self.env['excel.report'].create({
                'excel_file': base64.encodebytes(fp.getvalue()),
                'file_name': filename
            })
            fp.close()
            if report_id:
                return {
                    'view_mode': 'form',
                    'res_id': report_id.id,
                    'res_model': 'excel.report',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }

        else:
            raise UserError(
                _('No sales order for the selected vendor in this date range.'))
