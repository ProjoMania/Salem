# -*- encoding: utf-8 -*-
import io
import base64
import itertools

import xlwt
from odoo import models, fields, api, _
from odoo.exceptions import UserError

head_style = xlwt.easyxf(
    'font:bold True;pattern: pattern solid, fore_colour Tan;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
style1 = xlwt.easyxf(
    'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz center;')


class VendorSalesReport(models.TransientModel):
    _name = 'vendor.sales.report.wizard'

    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    excluded_vendor_ids = fields.Many2many('res.partner', string='Excluded Vendors',
                                           default=lambda self: self.env['res.partner'].search(
                                               [('auto_excluded', '=', True)]))
    filter_by = fields.Selection([('report_date', 'Report Date'), ('order_date', 'OrderDate'), ('both', 'Both')],
                                 string='Filter By', default='order_date', required=True)

    from_report_date = fields.Date(string="From date", tracking=True)
    to_report_date = fields.Date(string="To date", tracking=True)

    from_date = fields.Date(string="From date", tracking=True)
    to_date = fields.Date(string="To date", tracking=True)
    product_category_ids = fields.Many2many('product.category', string='Product Categories')
    stock_location_ids = fields.Many2many('stock.location', string='Stock Locations')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', check_company=True)
    exclude_product_ids = fields.Many2many('product.product', string='Excluded Products')

    def print_report_xls_menu(self):
        data, filename = self._prepare_report_data()
        return self._generate_excel_report(data, filename)

    # =====================[report data functions]=======================
    def _prepare_report_data(self):
        partner = self.vendor_id
        filename = 'Vendor Sales Report' + '.xls'
        res_company = self.env.company
        vendor_data_list = []
        end_date, start_date = self._prepare_start_end_date()
        suppliers_for_mail = self.env['product.supplierinfo'].sudo().search([("partner_id", "=", partner.id)])

        if suppliers_for_mail:
            products_list = self._prepare_product_list(suppliers_for_mail)
            stock_lines = self.env['stock.move.line'].sudo().search(
                self._prepare_move_domain(start_date, end_date, products_list))
            if stock_lines:
                lots_obj = self.env["stock.lot"].search([])
                sale_orders = self.env["sale.order"].search(self._prepare_sale_domain(start_date, end_date))
                ############################################################################################################
                move_type = 'out_invoice'
                ############################################################################################################
                invoice_line_ids = self.get_invoice_lines(sale_orders, start_date, end_date, products_list, move_type)

                for inv_line in invoice_line_ids:
                    lot_str = False
                    total_qty = 0
                    for line in inv_line.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                            lambda o: o.picking_id.backorder_id.id == False and o.picking_id.picking_type_code == 'outgoing' and o.picking_id.state == 'done'):
                        if line.quantity == inv_line.quantity and line.product_id == inv_line.product_id:
                            lot_str = line.lot_id.name
                            break
                        else:
                            continue
                    if not lot_str:
                        lot_str = False
                        total_qty = 0
                        for picking in inv_line.sale_line_ids.order_id.picking_ids.filtered(
                                lambda o: o.backorder_id.id == False and o.picking_type_code == 'outgoing' and o.state == 'done'):
                            total_qty = 0
                            for line in picking.move_line_ids_without_package:
                                if line.product_id == inv_line.product_id:
                                    lot_ids = inv_line.sale_line_ids.order_id.picking_ids.move_line_ids_without_package.filtered(
                                        lambda
                                            o: o.product_id == inv_line.product_id and o.picking_id.id == line.picking_id.id).mapped(
                                        'lot_id')
                                    if lot_ids:
                                        lots = lots_obj.search([("id", "in", lot_ids.ids)])
                                        lot_str = ''
                                        for lot in lots:
                                            lot_str += str(lot.name) + ', '
                    if inv_line:
                        vendor_based_data = {
                            "lot": lot_str if lot_str else "",
                            "vendor": partner.name if partner else "",
                            "invoice": inv_line.move_id.name if inv_line else "",
                            "sale_order": inv_line.sale_line_ids.order_id.name if inv_line.sale_line_ids.order_id.name else "",
                            "invoice_date": inv_line.move_id.invoice_date if self.filter_by == 'order_date' else inv_line.sale_line_ids.order_id.report_date,
                            "default_code": inv_line.product_id.default_code if inv_line.product_id.default_code else "",
                            "product_name": inv_line.product_id.name if inv_line.product_id.name else "",
                            "team_id": inv_line.move_id.team_id.name if inv_line.move_id.team_id.name else "",
                            "area": inv_line.move_id.partner_id.area if inv_line.move_id.partner_id.area else "",
                            "province": inv_line.move_id.partner_id.state_id.name if inv_line.move_id.partner_id.state_id.name else "",
                            "district": inv_line.move_id.partner_id.street if inv_line.move_id.partner_id.street else "",
                            "price_unit": inv_line.price_unit if inv_line.price_unit else "",
                            "customer_name": inv_line.move_id.partner_id.name if inv_line.move_id.partner_id.name else "",
                            "quantity": inv_line.quantity if inv_line.quantity else "0",
                            "price_subtotal": inv_line.price_subtotal if inv_line.price_subtotal else "0",
                            "currency": inv_line.currency_id.name if inv_line.currency_id.name else "",
                            "invoice_type": "Invoice",
                        }
                        vendor_data_list.append(vendor_based_data)
        data = {
            "company": res_company.name,
            "vendor_based": vendor_data_list,
            "start_date": start_date,
            "end_date": end_date
        }
        return data, filename

    def get_invoice_lines(self, sale_orders, start_date, end_date, products_list, move_type):
        if self.filter_by == 'order_date':
            return sale_orders.invoice_ids.invoice_line_ids.filtered(
                lambda
                    o: o.move_id.state != 'cancel' and o.product_id.id in products_list and
                       o.move_id.move_type == 'out_invoice' and
                       o.move_id.invoice_date >= start_date and
                       o.move_id.invoice_date <= end_date and
                       o.move_id.state != 'cancel')
        else:

            return sale_orders.invoice_ids.invoice_line_ids.filtered(
                lambda
                    o: o.move_id.state != 'cancel' and o.product_id.id in products_list and
                       o.move_id.move_type == 'out_invoice' and
                       o.report_date >= start_date and
                       o.report_date <= end_date and
                       o.move_id.state != 'cancel')

    def _prepare_start_end_date(self):
        if self.filter_by == 'order_date':
            start_date = self.from_date
            end_date = self.to_date
        else:
            start_date = self.from_report_date
            end_date = self.to_report_date
        return end_date, start_date

    def _prepare_move_domain(self, start_date, end_date, products_list):
        move_domain = []
        if self.filter_by == 'order_date':
            move_domain.append(("date", ">=", start_date))
            move_domain.append(("date", "<=", end_date))

        else:
            move_domain.append(("report_date", ">=", start_date))
            move_domain.append(("report_date", "<=", end_date))
        if products_list:
            move_domain.append(("product_id", "in", products_list))
        return move_domain

    def _prepare_sale_domain(self, start_date, end_date):
        sale_domain = []
        if self.filter_by == 'order_date':
            sale_domain.append(("date_order", ">=", start_date))
            sale_domain.append(("date_order", "<=", end_date))
        else:
            sale_domain.append(("report_date", ">=", start_date))
            sale_domain.append(("report_date", "<=", end_date))
        if self.excluded_vendor_ids:
            sale_domain.append(("partner_id", "not in", self.excluded_vendor_ids.ids))
        if self.warehouse_id:
            sale_domain.append(("warehouse_id", "=", self.warehouse_id.id))
        return sale_domain

    def _prepare_product_list(self, suppliers_for_mail):
        product_list = []
        env_product_product = self.env['product.product']
        product_domain = []
        if self.exclude_product_ids:
            product_domain.append(("id", "not in", self.exclude_product_ids.ids))
        if self.product_category_ids:
            product_domain.append(("categ_id", "in", self.product_category_ids.ids))
        for supplier in suppliers_for_mail:
            product = supplier.product_tmpl_id
            product_domain.append(("product_tmpl_id", "=", product.id))
            product_product = env_product_product.sudo().search(product_domain)
            product_list.append(product_product.ids)
        products_list = list(itertools.chain.from_iterable(product_list))
        return products_list

    # ===================================================================

    # ==========================[report functions]=======================
    def _generate_excel_report(self, data, filename):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Vendor Sales Report')
        head_style = xlwt.easyxf(
            'font:bold True;pattern: pattern solid, fore_colour Tan;align: horiz center; borders: top_color black, bottom_color black, right_color black, left_color black,left thin, right thin, top thin, bottom thin;')
        style1 = xlwt.easyxf(
            'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz center;')

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

    # ===================================================================
