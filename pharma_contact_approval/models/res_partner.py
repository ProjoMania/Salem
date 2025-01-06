from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    supervision_id = fields.Many2one('res.users', string='Supervisor')
    state = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], default='approved')
    is_approve = fields.Boolean("Is_approve")
    uids = fields.Integer(compute="_set_uid", store=True)
    
    def _set_uid(self):
        self.uids = self._context.get('uids')
        
    def approve_btn(self):
        for record in self:
            record.is_approve = True
            record.state = 'approved'
            
    @api.model
    def create(self, vals):
        vals['state'] = 'approved'
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if self.is_approve:
            vals['is_approve'] = False
            return super(ResPartner, self).write(vals)
        else:
            vals['state'] = 'pending'
            return super(ResPartner, self).write(vals)
        
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        if not self.env.user.has_group('base.group_erp_manager'):
            if not self.env.context.get('filter_partner'):
                domain += [('state', 'in', ['approved'])]
        return super()._search(domain, offset, limit, order, access_rights_uid)

