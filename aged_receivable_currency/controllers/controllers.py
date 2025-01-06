# -*- coding: utf-8 -*-
# from odoo import http


# class SaleAgedReceivableCurrency(http.Controller):
#     @http.route('/sale_aged_receivable_currency/sale_aged_receivable_currency', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_aged_receivable_currency/sale_aged_receivable_currency/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_aged_receivable_currency.listing', {
#             'root': '/sale_aged_receivable_currency/sale_aged_receivable_currency',
#             'objects': http.request.env['sale_aged_receivable_currency.sale_aged_receivable_currency'].search([]),
#         })

#     @http.route('/sale_aged_receivable_currency/sale_aged_receivable_currency/objects/<model("sale_aged_receivable_currency.sale_aged_receivable_currency"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_aged_receivable_currency.object', {
#             'object': obj
#         })

