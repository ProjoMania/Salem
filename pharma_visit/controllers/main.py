# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import http, models, tools, Command, _, fields

_logger = logging.getLogger()


class Visit(http.Controller):

    @http.route(['/visit/save_location'], type='json', auth='public')
    def save_location(self, cords, id=None):
        if id:
            visit_item = http.request.env['pharma.visit'].sudo().browse(id)
            visit_item.write({'partner_latitude': cords['latitude'], 'partner_longitude': cords['longitude']})
