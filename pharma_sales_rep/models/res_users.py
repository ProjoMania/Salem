
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    supervisor_id = fields.Many2one('res.users', string="Supervisor", domain=lambda self: [
        ("groups_id", "=", self.env.ref("pharma_sales_rep.group_supervisor").id)])
    manager_id = fields.Many2one('res.users', string="Manager", domain=lambda self: [
        ("groups_id", "=", self.env.ref("pharma_sales_rep.group_manager").id)])
