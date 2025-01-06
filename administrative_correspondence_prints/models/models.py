# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class administrative_correspondence_prints(models.Model):
#     _name = 'administrative_correspondence_prints.administrative_correspondence_prints'
#     _description = 'administrative_correspondence_prints.administrative_correspondence_prints'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

