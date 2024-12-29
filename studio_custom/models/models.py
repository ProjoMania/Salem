from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def comp_amount(self):
        records = self.search([('company_id', '=', 31), ('currency_id', '!=', 87), ('move_type', '!=', 'entry')])
        for rec in records:
            print(rec.line_ids.mapped('account_id'))
            print(rec.name)
            rec._compute_amount()
            print(rec.amount_untaxed_signed)
        return True


class Accountmoveline(models.Model):
    _inherit = "account.move.line"

    x_studio_field_uRnfp = fields.Selection(name="New Related Field", selection=[])


class Accountpayment(models.Model):
    _inherit = "account.payment"

    x_studio_field_Gb6C2 = fields.Many2one(name="Employee", comodel_name="hr.employee")
    x_studio_payment_type_ = fields.Char(name="طريقة السداد", )


class Hrapplicant(models.Model):
    _inherit = "hr.applicant"

    x_studio_field_9uX2K = fields.Selection(name="New Priority", selection=[('Very High', '3'), ('High', '2'),
                                                                            ('Low', '1'), ('Normal', '0')])
    x_studio_age = fields.Float(name="Age", )
    x_studio_years_or_experience = fields.Float(name="Years or Experience ", )
    x_studio_city = fields.Many2one(name="City", comodel_name="res.country.state")
    x_studio_photo = fields.Binary(name="Photo", )
    x_studio_field_lEDEP = fields.Float(name="New Decimal", )
    x_studio_field_of_study_1 = fields.Char(name="Field of Study", )


class Hrcontract(models.Model):
    _inherit = "hr.contract"

    x_studio_field_TqTNl = fields.Char(name="New Related Field", )


# class Hremployee(models.Model):
#     _inherit = "hr.employee"

   # x_studio_work_permit_expire = fields.Date(name="Work Permit Expire", )
   # x_studio_passport_expire = fields.Date(name="Passport Expire", )
    #x_studio_recidency_expire = fields.Date(name="Recidency Expire", )


class Hrpayslip(models.Model):
    _inherit = "hr.payslip"

    x_studio_city = fields.Char(name="City", )


class Purchaseorder(models.Model):
    _inherit = "purchase.order"

    x_studio_payment_type_ = fields.Char(name="Payment Type :", )
    x_studio_shipping_to_ = fields.Char(name="Shipping to :", )

    def ccompute_picking_ids(self):
        records = self.search([("company_id", '=', 31)])
        for rec in records:
            rec._compute_picking_ids()
            print(rec.picking_ids)
        return True


class Rescompany(models.Model):
    _inherit = "res.company"

    x_studio_background_report = fields.Binary(name="Background Report", )


class Stockmoveline(models.Model):
    _inherit = "stock.move.line"

    x_studio_demand = fields.Float(name="Demand", )
