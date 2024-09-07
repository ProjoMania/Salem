# -*- coding: utf-8 -*-
# from odoo import http


# class AdministrativeCorrespondencePrints(http.Controller):
#     @http.route('/administrative_correspondence_prints/administrative_correspondence_prints', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/administrative_correspondence_prints/administrative_correspondence_prints/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('administrative_correspondence_prints.listing', {
#             'root': '/administrative_correspondence_prints/administrative_correspondence_prints',
#             'objects': http.request.env['administrative_correspondence_prints.administrative_correspondence_prints'].search([]),
#         })

#     @http.route('/administrative_correspondence_prints/administrative_correspondence_prints/objects/<model("administrative_correspondence_prints.administrative_correspondence_prints"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('administrative_correspondence_prints.object', {
#             'object': obj
#         })

