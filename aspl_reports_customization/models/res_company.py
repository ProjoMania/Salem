from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO


class ResCompany(models.Model):
    _inherit = "res.company"


    def create_qr_code(self, model, id):
        # for rec in self:
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if qrcode and base64:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=4,
            )
            # name = self.env[model].search([('id', '=', id)])
            qr.add_data(str(url) + "/check_name_in_database?model=%s?%s" % (model, id))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
        return qr_image
