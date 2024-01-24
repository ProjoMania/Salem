# -*- coding: utf-8 -*-
# from odoo import http


# class StudioCustom(http.Controller):
#     @http.route('/studio_custom/studio_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/studio_custom/studio_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('studio_custom.listing', {
#             'root': '/studio_custom/studio_custom',
#             'objects': http.request.env['studio_custom.studio_custom'].search([]),
#         })

#     @http.route('/studio_custom/studio_custom/objects/<model("studio_custom.studio_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('studio_custom.object', {
#             'object': obj
#         })
