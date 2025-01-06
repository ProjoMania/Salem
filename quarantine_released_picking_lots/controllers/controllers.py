# -*- coding: utf-8 -*-
# from odoo import http


# class QuarantineReleasedPickingLots(http.Controller):
#     @http.route('/quarantine_released_picking_lots/quarantine_released_picking_lots', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quarantine_released_picking_lots/quarantine_released_picking_lots/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('quarantine_released_picking_lots.listing', {
#             'root': '/quarantine_released_picking_lots/quarantine_released_picking_lots',
#             'objects': http.request.env['quarantine_released_picking_lots.quarantine_released_picking_lots'].search([]),
#         })

#     @http.route('/quarantine_released_picking_lots/quarantine_released_picking_lots/objects/<model("quarantine_released_picking_lots.quarantine_released_picking_lots"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quarantine_released_picking_lots.object', {
#             'object': obj
#         })

