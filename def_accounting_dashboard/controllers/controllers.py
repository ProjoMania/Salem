# -*- coding: utf-8 -*-
# from odoo import http


# class DefAccountingDashboard(http.Controller):
#     @http.route('/def_accounting_dashboard/def_accounting_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/def_accounting_dashboard/def_accounting_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('def_accounting_dashboard.listing', {
#             'root': '/def_accounting_dashboard/def_accounting_dashboard',
#             'objects': http.request.env['def_accounting_dashboard.def_accounting_dashboard'].search([]),
#         })

#     @http.route('/def_accounting_dashboard/def_accounting_dashboard/objects/<model("def_accounting_dashboard.def_accounting_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('def_accounting_dashboard.object', {
#             'object': obj
#         })

