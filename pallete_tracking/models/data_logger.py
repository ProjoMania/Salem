# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class DataLogger(models.Model):
    _name = 'data.logger'
    _description = 'Data Logger'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'serial_number'

    serial_number = fields.Char(string="Data Logger Serial Number")
    pallets_no = fields.Many2one('stock.quant.package')
    create_date = fields.Date(string="Create Date")
    company = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    package_id = fields.Many2one('stock.quant.package')


class DataLoggerInherit(models.Model):
    _inherit = 'stock.move.line'

    data_logger = fields.Many2many('data.logger', string='Data Logger')

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        package_id = vals_list.get('package_id')
        if package_id:
            package = self.env['stock.quant.package'].browse(package_id)
            data_loggers = vals_list.get('data_logger', [])

            for logger in data_loggers:
                if logger and logger[2]:
                    package.logger_id = [(4, logger_id) for logger_id in
                                         logger[2]]
        return res

    def write(self, vals):
        res = super().write(vals)
        package_id = self.package_id
        if package_id:
            data_loggers = vals.get('data_logger', [])
            for logger in data_loggers:
                if logger and logger[2]:
                    logger_id = logger[2]
                    package_id.write({'logger_id': logger_id})
        return res


class DataLoggerStockPicking(models.Model):
    _inherit = 'stock.picking'

    driver_name = fields.Many2one('res.partner', string='Driver Name')
    vehicle_no = fields.Char(string="Vehicle No")
    pallet_no = fields.Char(string="Pallet No")
    arrived_date = fields.Datetime(string="Arrived Date")
    vehicle_temp = fields.Integer(string="Vehicle temp")
    vehicle_cleanliness = fields.Text(string="Vehicle Cleanliness")


class StockQuantPackageDataLogger(models.Model):
    _inherit = 'stock.quant.package'

    logger_id = fields.One2many('data.logger', 'pallets_no', string='Data Logger')

    @api.depends('quant_ids.location_id', 'quant_ids.company_id')
    def _compute_package_info(self):
        for package in self:
            package.company_id = self.env.company.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
