from odoo import models, fields, api, _


class Accountmove(models.Model):
    _inherit = "account.move"

    def compute_x_invoice_ids_payment_transaction_count(self):
        for record in self:
            record['x_invoice_ids_payment_transaction_count'] = self.env['payment.transaction'].search_count(
            [('invoice_ids', '=', record.id)])

    x_invoice_ids_payment_transaction_count = fields.Integer(string="Invoices count",
                                                             compute="compute_x_invoice_ids_payment_transaction_count")
    x_studio_po_bank_accounts = fields.Many2one(string="Bank Accounts", comodel_name="res.partner.bank")

    def compute_x_move_id_account_payment_count(self):
        for record in self: record['x_move_id_account_payment_count'] = self.env['account.payment'].search_count(
            [('move_id', '=', record.id)])

    x_move_id_account_payment_count = fields.Integer(string="Journal Entry count",
                                                     compute="compute_x_move_id_account_payment_count")
    x_studio_related_field_1gzOW = fields.Char(string="New Related Field", related="activity_user_id.name")
    x_studio_cash_collector = fields.Many2many(string="Cash Collector", comodel_name="res.users", relation="None",
                                               column1="account_move_id", column2="res_users_id")
    x_studio_state = fields.Many2one(string="state", related="partner_id.state_id", comodel_name="res.country.state")


class Accountmoveline(models.Model):
    _inherit = "account.move.line"

    x_studio_journal_entry_status = fields.Selection(string="Journal Entry Status",
                                                     selection="[('Draft', 'draft'), ('Posted', 'posted'), ('Cancelled', 'cancel')]",
                                                     related="move_id.state")
    x_studio_journal_type = fields.Selection(string="journal type",
                                             selection="[('Journal Entry', 'entry'), ('Customer Invoice', 'out_invoice'), ('Customer Credit Note', 'out_refund'), ('Vendor Bill', 'in_invoice'), ('Vendor Credit Note', 'in_refund'), ('Sales Receipt', 'out_receipt'), ('Purchase Receipt', 'in_receipt')]",
                                             related="move_id.move_type")
    x_studio_sales_team = fields.Many2one(string="Sales Team", related="move_id.team_id", comodel_name="crm.team")
    x_studio_related_field_TduGl = fields.Many2one(string="New Related Field", related="product_id.categ_id",
                                                   comodel_name="product.category")


class Accountpayment(models.Model):
    _inherit = "account.payment"

    x_studio_state = fields.Many2one(string="State", related="partner_id.state_id", comodel_name="res.country.state")


class Accountsetupbankmanualconfig(models.TransientModel):
    _inherit = "account.setup.bank.manual.config"

    x_studio_name_in_arabic = fields.Char(string="Name in Arabic",
                                          related="res_partner_bank_id.x_studio_name_in_arabic")


class Calendarevent(models.Model):
    _inherit = "calendar.event"

    x_studio_company = fields.Many2one(string="Company", related="user_id.company_id", comodel_name="res.company")


class Hrapplicant(models.Model):
    _inherit = "hr.applicant"

    x_studio_notes = fields.Text(string="Notes")
    x_studio_notes_1 = fields.Html(string="Notes:")


class Hrcontract(models.Model):
    _inherit = "hr.contract"

    x_studio_employee_company = fields.Many2one(string="Employee Company", related="employee_id.company_id",
                                                comodel_name="res.company")


class Hremployee(models.Model):
    _inherit = "hr.employee"

    x_studio_insurance_status = fields.Selection(string="Insurance Status",
                                                 selection="[('To Request', 'To Request'), ('Requested', 'Requested'), ('Active', 'Active'), ('Expired', 'Expired')]")
    x_studio_start_date = fields.Date(string="Start Date")
    x_studio_end_date = fields.Date(string="End Date")
    x_studio_insurance_type = fields.Selection(string="Insurance Type",
                                               selection="[('Normal', 'Normal'), ('VIP', 'VIP')]")
    x_studio_member_no = fields.Char(string="Member No")


class Hrexpense(models.Model):
    _inherit = "hr.expense"

    x_studio_number = fields.Char(string="Number")


class Hrexpensesheet(models.Model):
    _inherit = "hr.expense.sheet"

    x_studio_work_location = fields.Char(string="Work Location", related="employee_id.work_location_id.name")


class Hrpayslip(models.Model):
    _inherit = "hr.payslip"

    x_studio_related_field_2COEq = fields.Many2one(string="New Related Field", related="employee_id.address_id",
                                                   comodel_name="res.partner")
    x_studio_work_location = fields.Char(string="Work Location", related="employee_id.work_location_id.name")


class Productpricelist(models.Model):
    _inherit = "product.pricelist"

    x_studio_start_date = fields.Datetime(string="Start Date")
    x_studio_end_date = fields.Datetime(string="End Date")


class Producttemplate(models.Model):
    _inherit = "product.template"

    x_studio_bdk_sales_target = fields.Float(string="BDK Sales Target")
    x_studio_bdk_target = fields.Integer(string="BDK TARGET")


class Projecttask(models.Model):
    _inherit = "project.task"

    x_studio_many2one_field_kjo2d = fields.Many2one(string="Department", comodel_name="hr.department")
    x_studio_requested_by = fields.Many2many(string="Requested By", comodel_name="res.users", relation="x_project_task_res_users_rel",
                                             column1="project_task_id", column2="res_users_id")


class Purchaseorder(models.Model):
    _inherit = "purchase.order"

    x_studio_validate_by_job_title = fields.Char(string="Validate By Job Title")


class Respartnerbank(models.Model):
    _inherit = "res.partner.bank"

    x_studio_name_in_arabic = fields.Char(string="Name in Arabic")


class Saleorder(models.Model):
    _inherit = "sale.order"

    x_studio_state = fields.Many2one(string="state", related="partner_id.state_id", comodel_name="res.country.state")


class Stockmove(models.Model):
    _inherit = "stock.move"

    x_studio_valu_per_unit = fields.Float(string="Valu per unit",
                                             related="picking_id.move_ids_without_package.stock_valuation_layer_ids.stock_valuation_layer_ids.unit_cost")
    x_currency_id = fields.Many2one(string="Currency",
                                    related="picking_id.move_ids_without_package.stock_valuation_layer_ids.currency_id",
                                    comodel_name="res.currency")
    x_studio_stock_valuation_total = fields.Monetary(string="Stock Valuation total",
                                                     related="picking_id.move_ids_without_package.stock_valuation_layer_ids.value")


class Stockmoveline(models.Model):
    _inherit = "stock.move.line"

    x_studio_product_category = fields.Many2one(string="Product Category", related="product_id.categ_id",
                                                comodel_name="product.category")


class Stockpicking(models.Model):
    _inherit = "stock.picking"

    def compute_x_picking_id_stock_move_line_count(self):
        for record in self: record['x_picking_id_stock_move_line_count'] = self.env['stock.move.line'].search_count(
            [('picking_id', '=', record.id)])

    x_picking_id_stock_move_line_count = fields.Integer(string="Transfer count",
                                                        compute="compute_x_picking_id_stock_move_line_count")


class Stocklot(models.Model):
    _inherit = "stock.lot"

    x_studio_product_category = fields.Many2one(string="Product Category", related="product_id.categ_id",
                                                comodel_name="product.category")


class Stockvaluationlayer(models.Model):
    _inherit = "stock.valuation.layer"

    x_studio_type_of_opreation = fields.Selection(string="type of opreation",
                                                  selection="[('Receipt', 'incoming'), ('Delivery', 'outgoing'), ('Internal Transfer', 'internal'), ('Manufacturing', 'mrp_operation')]",
                                                  related="stock_move_id.picking_code")
    x_studio_journal_entry_status = fields.Selection(string="Journal Entry Status",
                                                     selection="[('Draft', 'draft'), ('Posted', 'posted'), ('Cancelled', 'cancel')]",
                                                     related="account_move_id.state")
    x_studio_journal_entry_status_1 = fields.Selection(string="Journal Entry Status",
                                                       selection="[('Draft', 'draft'), ('Posted', 'posted'), ('Cancelled', 'cancel')]",
                                                       related="account_move_id.state")


class StudioApprovalRule(models.Model):
    _inherit = "studio.approval.rule"

    def update_reg(self):
        records = self.search([])
        for rec in records:
            rec._update_registry()
        return True
