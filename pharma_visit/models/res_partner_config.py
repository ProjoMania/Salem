from odoo import models, fields


class DoctorSpeciality(models.Model):
    _name = "doctor.speciality"
    _rec_name = "name"

    name = fields.Char('Name')


class DoctorSubSpeciality(models.Model):
    _name = "doctor.sub_speciality"
    _rec_name = "name"

    name = fields.Char('Name')
    speciality_id = fields.Many2one("doctor.speciality", string='Speciality')


class Governorate(models.Model):
    _name = "governorate"
    _rec_name = "name"

    name = fields.Char('Name')


class Briks(models.Model):
    _name = "briks.briks"
    _rec_name = "name"

    name = fields.Char(string='Name')
    gov_id = fields.Many2one("governorate", string='Governorate')
    latitude = fields.Float(string='Latitude')
    longitude = fields.Float(string='Longitude')
    radius = fields.Integer(string='Radius')
