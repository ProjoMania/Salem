from odoo import models, fields, api, _
from datetime import datetime, timedelta


class Visit(models.Model):
    _name = "pharma.visit"
    _rec_name = 'partner_id'
    _inherit = ['mail.thread', 'timer.mixin']
    _description = "Visit"

    partner_id = fields.Many2one('res.partner', string="Doctor's Name")
    sales_rep_id = fields.Many2one('res.users', string='Sales Representative', domain=lambda self: [
        ("groups_id", "=", self.env.ref("pharma_sales_rep.group_sales_rep").id)])
    visit_type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')],
                                  required=True, default='weekly')
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7), tracking=True)
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7), tracking=True)
    start_time = fields.Datetime(string='Start Time')
    finish_time = fields.Datetime(string='End Time')
    time_spend = fields.Float(string='Time Spend', default=0.0)
    visit_count = fields.Integer(compute='compute_sale_order_count')
    promotion_id = fields.Many2one('visit.promotion')
    survey_id = fields.Many2one('survey.survey')
    state = fields.Selection([('draft', 'Draft'), ('exception', 'Exception'),
                              ('waiting_for_approval', 'Waiting For Approval'),
                              ('approved', 'Approved'),
                              ('done', 'Done')], default='draft')
    visit_line_ids = fields.One2many('visit.lines', 'visit_id')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    def compute_sale_order_count(self):
        for visit in self:
            visit.visit_count = self.env['visit.order'].search_count([('visit_id', '=', visit.id)])

    def action_timer_start(self):
        if not self.timer_start:
            self.write({'timer_start': fields.Datetime.now()})
        self.start_time = datetime.now()
        super().action_timer_start()

    def action_approved(self):
        self.state = "approved"

    def action_done(self):
        self.state = "done"

    def action_waiting_approval(self):
        self.state = "waiting_for_approval"

    def action_share(self):
        if self.survey_id:
            return self.survey_id.action_send_survey()

    def action_timer_stop(self):
        """ Stop the timer and return the spent minutes since it started
            :return minutes_spent if the timer is started,
                    otherwise return False
        """
        if not self.timer_start:
            return False
        minutes_spent = self._get_minutes_spent()
        self.finish_time = datetime.now()
        self.write({'timer_start': False, 'timer_pause': False})
        self.time_spend = minutes_spent
        super().action_timer_stop()
        return minutes_spent

    def _get_minutes_spent(self):
        start_time = self.timer_start
        stop_time = fields.Datetime.now()
        # timer was either running or paused
        if self.timer_pause:
            start_time += (stop_time - self.timer_pause)
        return (stop_time - start_time).total_seconds() / 60

    def create_visit_order(self):
        if self.visit_line_ids:
            partners = self.visit_line_ids.mapped('drug_store_id')
            for partner in partners:
                orders = self.visit_line_ids.filtered(lambda l: l.drug_store_id.id == partner.id)
                visit_order_lines = []
                for order in orders:
                    visit_order_lines.append((0, 0, {
                        'product_id': order.product_id.id,
                        'product_category_id': order.product_category_id.id,
                        'amount': order.amount,
                        'qty': order.qty,
                        'total': order.total,
                    }))

                visit_orders = self.env['visit.order'].create({
                    'drug_store_id': partner.id,
                    'partner_id': self.partner_id.id,
                    'sales_rep_id': self.sales_rep_id.id,
                    'order_date': datetime.today(),
                    'status': 'draft',
                    'visit_id': self.id,
                    'visit_order_ids': visit_order_lines,
                })

    def action_get_visit_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Visit Orders',
            'res_model': 'visit.order',
            'view_mode': 'tree,form',
            'domain': [('visit_id', '=', self.id)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.user.has_group('pharma_sales_rep.group_manager') or self.env.user.has_group(
                    'base.group_erp_manager'):
                vals['state'] = 'draft'
            else:
                vals['state'] = 'exception'
        return super().create(vals_list)
