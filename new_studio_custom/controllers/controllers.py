# -*- coding: utf-8 -*-
# from odoo import http


# class NewStudioCustom(http.Controller):
#     @http.route('/new_studio_custom/new_studio_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_studio_custom/new_studio_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_studio_custom.listing', {
#             'root': '/new_studio_custom/new_studio_custom',
#             'objects': http.request.env['new_studio_custom.new_studio_custom'].search([]),
#         })

#     @http.route('/new_studio_custom/new_studio_custom/objects/<model("new_studio_custom.new_studio_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_studio_custom.object', {
#             'object': obj
#         })

