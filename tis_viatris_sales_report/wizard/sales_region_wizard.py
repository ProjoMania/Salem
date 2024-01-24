# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2022. All rights reserved.

from odoo import fields, models, _
from datetime import datetime
# import xlwt
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf
from odoo.osv import expression
from odoo.tools.misc import format_datetime
from dateutil import relativedelta


class ViatrisSalesReport(models.TransientModel):
    _name = 'viatris.sales.report'

    from_date = fields.Date(string="From date", tracking=True, required=True)
    to_date = fields.Date(string="To date", tracking=True, required=True)
    customer_id = fields.Many2many('res.partner', string="With Out Customer")
    product_category_id = fields.Many2one('product.category',
                                          string="Product Category")

    def print_button(self):
        results = 0
        from_date = self.from_date
        to_date = self.to_date
        customer_id = self.customer_id
        user_name = 0
        return self.with_context(discard_logo_check=True).report_xls(results,
                                                                     customer_id,)

    def report_xls(self, results, customer_id):
        if self.product_category_id:
            product_categories = self.env['product.category'].search(
                [('id', 'child_of', self.product_category_id.id)])
            products = self.env['product.product'].search(
                [('categ_id', 'in', product_categories.ids)])
        else:
            products = self.env['product.product'].search([])
        print("products", products)
        warehouse_ids = self.env['stock.warehouse'].search(
            [('hide_in_viatris_report', '!=', True)])
        warehouse_count = len(warehouse_ids)
        sale_region_ids = self.env['sales.region'].search([])
        sale_region_count = len(sale_region_ids)
        print("sale_region_ids", sale_region_ids, sale_region_count)
        locations_ids = self.env['stock.location'].search([])

        filename = 'Viatris Sales Report' + '.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Viatris Sales Report',
                                       cell_overwrite_ok=True)
        format_3 = easyxf(
            'font:bold True;font:height 220;')
        format_6 = easyxf(
            'font:bold True;font:height 280; align: horiz center; borders:  top thin, left thin,,bottom thin, right thin;')
        format_4 = easyxf(
            'font:bold True;font:height 220; align: horiz left;  borders:  top thin, left thin,,bottom thin, right thin;')
        format_2 = easyxf(
            'font:bold True;font:height 220; align: horiz center;  borders:  top thin, left thin,,bottom thin, right thin;')
        format_1 = easyxf(
            'font:bold True; font:height 350; align: horiz center;borders:  bottom medium, top medium;')
        format_5 = easyxf(
            'font:bold True;font:height 220;font:color red; align: horiz left;  borders:  top thin, left thin,,bottom thin, right thin;')
        format_6 = easyxf(
            'font:bold True;font:height 220;font:color blue; align: horiz left;  borders:  top thin, left thin,,bottom thin, right thin;')
        worksheet.col(0).width = 8000
        worksheet.col(1).width = 8000
        worksheet.col(2).width = 8000
        worksheet.col(3).width = 8000
        worksheet.col(4).width = 8000
        row = 0
        col_n = 0
        worksheet.write(0, 0, 'Vendor')
        worksheet.write(0, 1, self.product_category_id.name)
        # worksheet.write(1, 0, 'without customer', format_3)
        col = 1
        cust_str = str(customer_id.ids)
        cust_str = cust_str.replace('[', '(')
        cust_str = cust_str.replace(']', ')')
        # for customer in customer_id:
        #     worksheet.write(1, col, customer.name, format_3)
        #     col += 1
        worksheet.write(1, 0, 'From :', format_3)
        worksheet.write(1, 1, str(self.from_date), format_3)
        worksheet.write(2, 0, 'To :', format_3)
        worksheet.write(2, 1, str(self.to_date), format_3)
        worksheet.write_merge(4, 5, 0, 0, 'Code', format_4)
        worksheet.write_merge(6, 6, 0, 0, 'Code', format_4)
        worksheet.write_merge(4, 6, 1, 1, 'SKU', format_4)
        worksheet.write_merge(4, 6, 2, 2, 'NSP $', format_4)
        worksheet.write_merge(4, 4, 3, 2 + warehouse_count,
                              'Opening Stock QTY', format_2)
        col = 3
        for warehouse in warehouse_ids:
            worksheet.write_merge(5, 6, col, col, warehouse.name, format_4)
            col = col + 1
        worksheet.write_merge(4, 4, col, col - 1 + warehouse_count,
                              'New shipment received QTY ', format_2)
        for warehouse in warehouse_ids:
            worksheet.write_merge(5, 6, col, col, warehouse.name, format_4)
            col = col + 1
        worksheet.write_merge(4, 4, col, col - 1 + warehouse_count,
                              'Transfers QTY', format_2)
        for warehouse in warehouse_ids:
            worksheet.write_merge(5, 6, col, col, warehouse.name, format_4)
            col = col + 1
        worksheet.write_merge(4, 4, col, col - 1 + sale_region_count * 2,
                              'Sales Unit', format_2)
        for sale_region in sale_region_ids:
            worksheet.write_merge(5, 5, col, col + 1, sale_region.name,
                                  format_4)
            worksheet.write(6, col, 'Unit', format_6)
            worksheet.write(6, col + 1, 'Free', format_5)
            col = col + 2
        worksheet.write(4, col, 'QTY ', format_2)
        worksheet.write_merge(5, 6, col, col, 'Total sales unit', format_6)
        col = col + 1
        worksheet.write(4, col, ' ', format_2)
        worksheet.write_merge(5, 6, col, col, 'Total Free unit', format_5)
        col = col + 1
        worksheet.write(4, col, ' ', format_2)
        worksheet.write_merge(5, 6, col, col, 'Total sales value in usd $',
                              format_2)
        col = col + 1
        worksheet.write_merge(4, 4, col, col - 1 + warehouse_count * 2,
                              'Closing Stock', format_2)
        for warehouse in warehouse_ids:
            worksheet.write_merge(5, 6, col, col, warehouse.name, format_4)
            col = col + 1
            worksheet.write_merge(5, 6, col, col, 'Sellable', format_4)
            col = col + 1
        worksheet.write_merge(4, 6, col, col, 'Total closing stock', format_2)
        product_row = 7
        for product in products:
            product_col = 0
            worksheet.write(product_row, product_col, product.default_code,
                            format_2)
            product_col = product_col + 1
            worksheet.write(product_row, product_col, product.name, format_2)
            product_col = product_col + 1
            worksheet.write(product_row, product_col, product.list_price,
                            format_2)
            product_col = product_col + 1
            for warehouse1 in warehouse_ids:
                total_onhand_qty = product.with_context(
                    {'warehouse': warehouse1.id,
                     'to_date': self.from_date}).qty_available
                worksheet.write(product_row, product_col, total_onhand_qty,
                                format_2)
                product_col = product_col + 1
            list_qty = []
            for warehouse in warehouse_ids:
                total_receive_qty = 0
                for location in locations_ids:
                    if location.warehouse_id == warehouse and location.usage == 'internal':
                        if self.customer_id:
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                                                                                inner join stock_picking as picking on line.picking_id = picking.id
                                                                                                inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                                                                                where type_1.code='incoming'
                                                                                                and line.product_id =%s
                                                                                                and picking.date <= '%s' and picking.date >= '%s'
                                                                                                and picking.location_dest_id =%s
                                                                                                and picking.partner_id in %s
                                                                                                group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id, cust_str)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                total_receive_qty = total_receive_qty + res[0][
                                    1]
                            pro_move = self.env['stock.move.line'].search(
                                ["&", "&", "&", "&", "&",
                                 ("state", "=", "done"), (
                                 "picking_id.picking_type_id.code", "=",
                                 "incoming"),
                                 ("picking_id.partner_id", "not in", cust_str),
                                 "&", ["date", ">=", self.from_date],
                                 ["date", "<=", self.to_date],
                                 ['product_id', '=', product.id],
                                 ['location_dest_id', '=', location.id]])
                            list_qty = pro_move.mapped('qty_done')

                        else:
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                                                    inner join stock_picking as picking on line.picking_id = picking.id
                                                                    inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                                                    where type_1.code='incoming'
                                                                    and line.product_id =%s
                                                                    and line.date <= '%s' and line.date >= '%s"'
                                                                    and picking.location_dest_id =%s
                                                                    group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                total_receive_qty = total_receive_qty + res[0][
                                    1]
                            pro_move = self.env['stock.move.line'].search(
                                ["&", "&", "&", "&", ("state", "=", "done"), (
                                "picking_id.picking_type_id.code", "=",
                                "incoming"), "&",
                                 ["date", ">=", self.from_date],
                                 ["date", "<=", self.to_date],
                                 ['product_id', '=', product.id],
                                 ['location_dest_id', '=', location.id]])
                            list_qty = pro_move.mapped('qty_done')
                    if list_qty:
                        total_receive_qty = total_receive_qty + sum(list_qty)
                worksheet.write(product_row, product_col, total_receive_qty,
                                format_2)
                product_col = product_col + 1
            for warehouse in warehouse_ids:
                total_internal_qty = 0
                for location in locations_ids:
                    if location.warehouse_id == warehouse and location.usage == 'internal':
                        if self.customer_id:
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                                                    inner join stock_picking as picking on line.picking_id = picking.id
                                                                    inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                                                    where type_1.code='internal'
                                                                    and line.product_id =%s
                                                                    and picking.date <= '%s' and picking.date >= '%s'
                                                                    and picking.location_id =%s
                                                                    and picking.partner_id in %s
                                                                    group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id, cust_str)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                print("ffffffffffff",product.name,res[0][1])
                                total_internal_qty = - (total_internal_qty +res[0][1])
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                                                                                inner join stock_picking as picking on line.picking_id = picking.id
                                                                                                inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                                                                                where type_1.code='internal'
                                                                                                and line.product_id =%s
                                                                                                and picking.date <= '%s' and picking.date >= '%s'
                                                                                                and picking.location_dest_id =%s
                                                                                                and picking.partner_id in %s
                                                                                                group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id, cust_str)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                total_internal_qty = total_internal_qty + \
                                                     res[0][1]
                                print("ffffffffffff", product.name, res[0][1])
                        else:
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                        inner join stock_picking as picking on line.picking_id = picking.id
                                        inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                        where type_1.code='internal'
                                        and line.product_id =%s
                                        and picking.date <= '%s' and picking.date >= '%s'
                                        
                                        and picking.location_dest_id =%s
                                        group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                total_internal_qty = total_internal_qty + \
                                                     res[0][1]
                            query = """ select line.product_id,sum(line.qty_done),picking.location_id,type_1.code from stock_move_line as line
                                                                    inner join stock_picking as picking on line.picking_id = picking.id
                                                                    inner join stock_picking_type as type_1 on picking.picking_type_id = type_1.id
                                                                    where type_1.code='internal'
                                                                    and line.product_id =%s
                                                                    and picking.date <= '%s' and picking.date >= '%s'

                                                                    and picking.location_dest_id =%s
                                                                    group by line.product_id,picking.location_id,type_1.code """ % (
                                product.id, self.to_date, self.from_date,
                                location.id)
                            self.env.cr.execute(query)
                            res = self.env.cr.fetchall()
                            if len(res) == 0:
                                pass
                            else:
                                total_internal_qty = -(total_internal_qty +res[0][1])
                worksheet.write(product_row, product_col, total_internal_qty,
                                format_2)
                product_col = product_col + 1

            from_date_time = datetime.combine(self.from_date,
                                              datetime.min.time())
            to_date_time = datetime.combine(self.to_date, datetime.min.time())
            total_unit_count = 0
            total_free_unit_count = 0
            for sale_region in sale_region_ids:
                total_sale_order = 0
                total_free_sale_order = 0

                sales_teams = self.env['crm.team'].search(
                    [('sales_region_id', '=', sale_region.id)])
                lst_str = str(sales_teams.ids)
                lst_str = lst_str.replace('[', '(')
                lst_str = lst_str.replace(']', ')')
                cust_str = str(customer_id.ids)
                cust_str = cust_str.replace('[', '(')
                cust_str = cust_str.replace(']', ')')
                if self.customer_id:
                    # print("ggggggggggggggggggggggggg",self.customer_id)
                    if sales_teams:
                        # print("kkkkkkkkkkkkkkkkkkkggggggggggggggggg",sale_region,sales_teams)
                        # query = """ SELECT
                        #                         line.product_id,
                        #                         template.name,
                        #                        sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
                        #                                                                                     AS quantity
                        #                                                                                      FROM account_move_line line
                        #                         LEFT JOIN res_partner partner ON partner.id = line.partner_id
                        #                         LEFT JOIN product_product product ON product.id = line.product_id
                        #                         LEFT JOIN account_account account ON account.id = line.account_id
                        #                         LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                        #                         LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                        #                         LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                        #                         LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                        #                         INNER JOIN account_move move ON move.id = line.move_id
                        #                         LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                        #                         JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
                        #     currency_table=self.env[
                        #         'res.currency']._get_query_currency_table(
                        #         {'multi_company': True,
                        #          'date': {'date_to': fields.Date.today()}}),
                        # )
                        #
                        # query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                        #                         AND line.account_id IS NOT NULL
                        #                         and invoice_date <= '%s' and invoice_date >= '%s'
                        #                         AND NOT line.exclude_from_invoice_tab
                        #                         and line.product_id =%s
                        #                         and line.price_unit != 0
                        #                         and move.team_id in %s
                        #                         and line.partner_id in %s
                        #                         group by line.product_id,template.name """ % (
                        #     self.to_date, self.from_date, product.id, lst_str,
                        #     cust_str)
                        # self.env.cr.execute(query)
                        # res = self.env.cr.fetchall()

                        move_ids = self.env['account.move.line'].search(["&", (
                        "move_id.state", "not in",
                        ("move_id.draft", "cancel")), "&", "|", (
                                                                         "move_id.move_type",
                                                                         "=",
                                                                         "out_invoice"),
                                                                         (
                                                                         "move_id.move_type",
                                                                         "=",
                                                                         "out_refund"),
                                                                         "&", (
                                                                         "product_id.categ_id",
                                                                         "=",
                                                                         self.product_category_id.id),
                                                                         (
                                                                             'move_id.partner_id',
                                                                             '!=',
                                                                             self.customer_id.id)])
                        lst_qty = move_ids.search(
                            [('move_id.team_id', 'in', sales_teams.ids),
                             ('product_id', '=', product.id),
                             ('move_id.invoice_date', '>=', self.from_date),
                             ('move_id.invoice_date', '<=', self.to_date),
                             ('price_unit', '!=', 0), (
                             'move_id.partner_id', '!=',
                             self.customer_id.id)]).mapped('quantity')
                        total_qty = sum(lst_qty)
                        worksheet.write(product_row, product_col, total_qty,
                                        format_2)
                        product_col = product_col + 1
                        lst_qty = move_ids.search(
                            [('move_id.team_id', 'in', sales_teams.ids),
                             ('product_id', '=', product.id),
                             ('move_id.invoice_date', '>=', self.from_date),
                             ('move_id.invoice_date', '<=', self.to_date),
                             ('price_unit', '=', 0), (
                             'move_id.partner_id', '!=',
                             self.customer_id.id)]).mapped('quantity')
                        total_qty = sum(lst_qty)
                        worksheet.write(product_row, product_col, total_qty,
                                        format_2)
                        product_col = product_col + 1

                        # if len(res) == 0:
                        #     worksheet.write(product_row, product_col, 0,
                        #                     format_2)
                        # else:
                        #     worksheet.write(product_row, product_col,
                        #                     res[0][2], format_2)
                else:
                    move_ids = self.env['account.move.line'].search(["&", (
                        "move_id.state", "not in",
                        ("move_id.draft", "cancel")),
                                                                     "&", "|",
                                                                     (
                                                                         "move_id.move_type",
                                                                         "=",
                                                                         "out_invoice"),
                                                                     (
                                                                         "move_id.move_type",
                                                                         "=",
                                                                         "out_refund"),
                                                                      (
                                                                         "product_id.categ_id",
                                                                         "=",
                                                                         self.product_category_id.id)])
                    lst_qty = move_ids.search(
                        [('move_id.team_id', 'in', sales_teams.ids),
                         ('product_id', '=', product.id),
                         ('move_id.invoice_date', '>=', self.from_date),
                         ('move_id.invoice_date', '<=', self.to_date),
                         ('price_unit', '!=', 0)]).mapped(
                        'quantity')
                    total_qty = sum(lst_qty)
                    worksheet.write(product_row, product_col, total_qty,
                                    format_2)
                    product_col = product_col + 1
                    lst_qty = move_ids.search(
                        [('move_id.team_id', 'in', sales_teams.ids),
                         ('product_id', '=', product.id),
                         ('move_id.invoice_date', '>=', self.from_date),
                         ('move_id.invoice_date', '<=', self.to_date),
                         ('price_unit', '=', 0)]).mapped(
                        'quantity')
                    total_qty = sum(lst_qty)
                    worksheet.write(product_row, product_col, total_qty,
                                    format_2)
                    product_col = product_col + 1

                    # if sales_teams:
                    #     query = """ SELECT
                    #         line.product_id,
                    #         template.name,
                    #        sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
                    #                                                                     AS quantity
                    #                                                                      FROM account_move_line line
                    #         LEFT JOIN res_partner partner ON partner.id = line.partner_id
                    #         LEFT JOIN product_product product ON product.id = line.product_id
                    #         LEFT JOIN account_account account ON account.id = line.account_id
                    #         LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                    #         LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                    #         LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                    #         LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                    #         INNER JOIN account_move move ON move.id = line.move_id
                    #         LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                    #         JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
                    #         currency_table=self.env[
                    #             'res.currency']._get_query_currency_table(
                    #             {'multi_company': True,
                    #              'date': {'date_to': fields.Date.today()}}),
                    #     )
                    #
                    #     query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                    #         AND line.account_id IS NOT NULL
                    #         and invoice_date <= '%s' and invoice_date >= '%s'
                    #         AND NOT line.exclude_from_invoice_tab
                    #         and line.product_id =%s
                    #         and line.price_unit != 0
                    #         and move.team_id in %s
                    #         group by line.product_id,template.name """ % (
                    #         self.to_date, self.from_date, product.id, lst_str)
                    #     self.env.cr.execute(query)
                    #     res = self.env.cr.fetchall()
                    #
                    #     if len(res) == 0:
                    #         worksheet.write(product_row, product_col, 0,
                    #                         format_2)
                    #     else:
                    #         worksheet.write(product_row, product_col,
                    #                         res[0][2], format_2)
                    #     product_col = product_col + 1
                # if self.customer_id:
                #     if sales_teams:
                #         query = """ SELECT
                #                                                     line.product_id,
                #                                                     template.name,
                #                                                    sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
                #                                                                                                                 AS quantity
                #                                                                                                                  FROM account_move_line line
                #                                                     LEFT JOIN res_partner partner ON partner.id = line.partner_id
                #                                                     LEFT JOIN product_product product ON product.id = line.product_id
                #                                                     LEFT JOIN account_account account ON account.id = line.account_id
                #                                                     LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                #                                                     LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                #                                                     LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                #                                                     LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                #                                                     INNER JOIN account_move move ON move.id = line.move_id
                #                                                     LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                #                                                     JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
                #             currency_table=self.env[
                #                 'res.currency']._get_query_currency_table(
                #                 {'multi_company': True,
                #                  'date': {'date_to': fields.Date.today()}}),
                #         )
                #
                #         query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                #                                                     AND line.account_id IS NOT NULL
                #                                                     and invoice_date <= '%s' and invoice_date >= '%s'
                #                                                     AND NOT line.exclude_from_invoice_tab
                #                                                     and line.product_id =%s
                #                                                     and line.price_unit = 0
                #                                                     and move.team_id in %s
                #                                                     and line.partner_id in %s
                #                                                     group by line.product_id,template.name """ % (
                #             self.to_date, self.from_date, product.id, lst_str,
                #             cust_str)
                #         self.env.cr.execute(query)
                #         res = self.env.cr.fetchall()
                #
                #         if len(res) == 0:
                #             worksheet.write(product_row, product_col, 0,
                #                             format_2)
                #         else:
                #             worksheet.write(product_row, product_col,
                #                             res[0][2], format_2)
                # else:
                #     if sales_teams:
                #         query = """ SELECT
                #                                 line.product_id,
                #                                 template.name,
                #                                sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
                #                                                                                             AS quantity
                #                                                                                              FROM account_move_line line
                #                                 LEFT JOIN res_partner partner ON partner.id = line.partner_id
                #                                 LEFT JOIN product_product product ON product.id = line.product_id
                #                                 LEFT JOIN account_account account ON account.id = line.account_id
                #                                 LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                #                                 LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                #                                 LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                #                                 LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                #                                 INNER JOIN account_move move ON move.id = line.move_id
                #                                 LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                #                                 JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
                #             currency_table=self.env[
                #                 'res.currency']._get_query_currency_table(
                #                 {'multi_company': True,
                #                  'date': {'date_to': fields.Date.today()}}),
                #         )
                #
                #         query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                #                                 AND line.account_id IS NOT NULL
                #                                 and invoice_date <= '%s' and invoice_date >= '%s'
                #                                 AND NOT line.exclude_from_invoice_tab
                #                                 and line.product_id =%s
                #                                 and line.price_unit = 0
                #                                 and move.team_id in %s
                #                                 group by line.product_id,template.name """ % (
                #             self.to_date, self.from_date, product.id, lst_str)
                #         self.env.cr.execute(query)
                #         res = self.env.cr.fetchall()
                #
                #         if len(res) == 0:
                #             worksheet.write(product_row, product_col, 0,
                #                             format_2)
                #         else:
                #             worksheet.write(product_row, product_col,
                #                             res[0][2], format_2)
                #         # worksheet.write(product_row, product_col, total_unit_count, format_2)
                #         product_col = product_col + 1
            # query = """ SELECT
            #                         line.product_id,
            #                         template.name,
            #                        sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
            #                                                                                     AS quantity
            #                                                                                      FROM account_move_line line
            #                         LEFT JOIN res_partner partner ON partner.id = line.partner_id
            #                         LEFT JOIN product_product product ON product.id = line.product_id
            #                         LEFT JOIN account_account account ON account.id = line.account_id
            #                         LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
            #                         LEFT JOIN product_template template ON template.id = product.product_tmpl_id
            #                         LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
            #                         LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
            #                         INNER JOIN account_move move ON move.id = line.move_id
            #                         LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
            #                         JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
            #     currency_table=self.env[
            #         'res.currency']._get_query_currency_table(
            #         {'multi_company': True,
            #          'date': {'date_to': fields.Date.today()}}),
            # )
            #
            # query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
            #             AND line.account_id IS NOT NULL
            #             and invoice_date <= '%s' and invoice_date >= '%s'
            #             AND NOT line.exclude_from_invoice_tab
            #             and line.product_id =%s
            #             and line.price_unit != 0
            #             group by line.product_id,template.name """ % (
            #     self.to_date, self.from_date, product.id)
            # self.env.cr.execute(query)
            # res = self.env.cr.fetchall()
            #
            # if len(res) == 0:
            #     worksheet.write(product_row, product_col, 0, format_2)
            # else:
            #     # worksheet.write(product_row, product_col, res[0][2], format_2)
            #     worksheet.write(product_row, product_col, 123, format_2)
            # # worksheet.write(product_row, product_col, total_unit_count, format_2)
            move_ids = self.env['account.move.line'].search(
                ["&", ("move_id.state", "not in", ("move_id.draft", "cancel")),
                 "&", "|", ("move_id.move_type", "=", "out_invoice"),
                 ("move_id.move_type", "=", "out_refund"), "&",
                 ("product_id.categ_id", "=", self.product_category_id.id),
                 ("move_id.partner_id", "not ilike", "BDK")])
            lst_qty = move_ids.search(
                [('product_id', '=', product.id),
                 ('move_id.invoice_date', '>=', self.from_date),
                 ('move_id.invoice_date', '<=', self.to_date),
                 ('price_unit', '!=', 0),
                 ('move_id.partner_id', '!=', self.customer_id.id)]).mapped(
                'quantity')
            total_qty = sum(lst_qty)
            worksheet.write(product_row, product_col, total_qty,
                            format_2)
            product_col = product_col + 1
            lst_qty = move_ids.search(
                [
                    ('product_id', '=', product.id),
                    ('move_id.invoice_date', '>=', self.from_date),
                    ('move_id.invoice_date', '<=', self.to_date),
                    ('price_unit', '=', 0),
                    ('move_id.partner_id', '!=', self.customer_id.id)]).mapped(
                'quantity')
            total_qty = sum(lst_qty)
            worksheet.write(product_row, product_col, total_qty,
                            format_2)
            product_col = product_col + 1
            query = """ SELECT
                                    line.product_id,
                                    template.name,
                                   sum( line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0) * (CASE WHEN move.move_type IN ('in_invoice','out_refund','in_receipt') THEN -1 ELSE 1 END))
                                                                                                AS quantity
                                                                                                 FROM account_move_line line
                                    LEFT JOIN res_partner partner ON partner.id = line.partner_id
                                    LEFT JOIN product_product product ON product.id = line.product_id
                                    LEFT JOIN account_account account ON account.id = line.account_id
                                    LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                                    LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                                    LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                                    LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                                    INNER JOIN account_move move ON move.id = line.move_id
                                    LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
                                    JOIN {currency_table} ON currency_table.company_id = line.company_id""".format(
                currency_table=self.env[
                    'res.currency']._get_query_currency_table(
                    {'multi_company': True,
                     'date': {'date_to': fields.Date.today()}}),
            )

            query += """ WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                        AND line.account_id IS NOT NULL
                        and invoice_date <= '%s' and invoice_date >= '%s'
                        AND NOT line.exclude_from_invoice_tab
                        and line.product_id =%s
                        and line.price_unit = 0
                        group by line.product_id,template.name """ % (
                self.to_date, self.from_date, product.id)
            self.env.cr.execute(query)
            res = self.env.cr.fetchall()
            # if len(res) == 0:
            #     worksheet.write(product_row, product_col, 0, format_2)
            # else:
            #     worksheet.write(product_row, product_col, res[0][2], format_2)
            # product_col = product_col + 1
            total_sales_value = total_unit_count * product.list_price
            worksheet.write(product_row, product_col, total_sales_value,
                            format_2)
            product_col = product_col + 1
            total_closing_stock = 0
            for warehouse in warehouse_ids:
                total_onhand_qty = 0
                total_onhand_qty = product.with_context(
                    {'warehouse': warehouse.id, 'from_date': self.from_date,
                     'to_date': self.to_date}).qty_available
                total_closing_stock = total_closing_stock + total_onhand_qty
                worksheet.write(product_row, product_col, total_onhand_qty,
                                format_2)
                product_col = product_col + 1
                total_receive_qty = 0
                total_delivery_qty = 0
                for location in locations_ids:
                    if location.warehouse_id == warehouse and location.usage == 'internal':
                        if self.customer_id:
                            picking_ids = self.env['stock.picking'].search(
                                [('location_id', '=', location.id),
                                 ('product_id', '=', product.id),
                                 ('picking_type_code', '=', 'outgoing'),
                                 ('date', '>=', self.from_date),
                                 ('date', '<=', self.to_date),
                                 ('partner_id', 'not in', customer_id.ids)])
                        else:
                            picking_ids = self.env['stock.picking'].search(
                                [('location_id', '=', location.id),
                                 ('product_id', '=', product.id),
                                 ('picking_type_code', '=', 'outgoing'),
                                 ('date', '>=', self.from_date),
                                 ('date', '<=', self.to_date)])
                        # for picking in picking_ids:
                        #     for move_id_without_package in picking.move_ids_without_package:
                        #         if move_id_without_package:
                        #             total_delivery_qty = move_id_without_package.quantity_done + total_delivery_qty
                # worksheet.write(product_row, product_col, total_delivery_qty,
                #                 format_2)
                worksheet.write(product_row, product_col, total_delivery_qty,
                                format_2)
                product_col = product_col + 1
            worksheet.write(product_row, product_col, total_closing_stock,
                            format_2)
            product_row = product_row + 1

        print("product_row", product_row)
        if self.product_category_id:
            scrap_row = product_row + 4
            scrap_head_style = easyxf(
                'font:bold True;font:height 350; align: horiz center;  borders:  top thin, left thin,,bottom thin, right thin;')
            worksheet.write_merge(scrap_row, scrap_row + 2, 1, 4, 'SCRAP',
                                  scrap_head_style)
            product_categories = self.env['product.category'].search(
                [('id', 'child_of', self.product_category_id.id)])
            products = self.env['product.product'].search(
                [('categ_id', 'in', product_categories.ids)])
            scrap_ids = self.env['stock.scrap'].search(
                [('product_id', 'in', products.ids),
                 ('date_done', '>=', self.from_date),
                 ('date_done', '<=', self.to_date)])
            print("scrap_ids", scrap_ids)
            scrap_pdt_row = scrap_row + 3
            if scrap_ids:
                worksheet.write_merge(scrap_row, scrap_row + 2, 1, 4, 'SCRAP',
                                      scrap_head_style)
                worksheet.write(scrap_pdt_row, 1, 'Products', format_2)
                worksheet.write(scrap_pdt_row, 2, 'Location', format_2)
                worksheet.write(scrap_pdt_row, 3, 'Batch/ Lot', format_2)
                worksheet.write(scrap_pdt_row, 4, 'Qty', format_2)
                row = scrap_pdt_row + 1
                col = 0
                for rec in scrap_ids:
                    worksheet.write(row, col + 1, rec.name, format_2)
                    worksheet.write(row, col + 2, rec.scrap_location_id.name,
                                    format_2)
                    worksheet.write(row, col + 3, rec.lot_id.name,
                                    format_2)
                    worksheet.write(row, col + 4, rec.scrap_qty, format_2)
                    row += 1
        fp = io.BytesIO()
        workbook.save(fp)
        report_id = self.env['excel.report'].create({
            'excel_file': base64.encodebytes(fp.getvalue()),
            'file_name': filename
        })
        fp.close()

        return {
            'view_mode': 'form',
            'res_id': report_id.id,
            'res_model': 'excel.report',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
