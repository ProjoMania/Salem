from odoo import models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    def _check_current_contract(self):
        """
        Override the original method to disable contract overlap validation.
        This allows employees to have multiple active contracts simultaneously.
        """
        # Do nothing - this disables the constraint
        pass 