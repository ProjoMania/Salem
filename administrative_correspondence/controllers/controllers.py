# -*- coding: utf-8 -*-
# from odoo import http


# class AdministrativeCorrespondence(http.Controller):
#     @http.route('/administrative_correspondence/administrative_correspondence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/administrative_correspondence/administrative_correspondence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('administrative_correspondence.listing', {
#             'root': '/administrative_correspondence/administrative_correspondence',
#             'objects': http.request.env['administrative_correspondence.administrative_correspondence'].search([]),
#         })

#     @http.route('/administrative_correspondence/administrative_correspondence/objects/<model("administrative_correspondence.administrative_correspondence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('administrative_correspondence.object', {
#             'object': obj
#         })
