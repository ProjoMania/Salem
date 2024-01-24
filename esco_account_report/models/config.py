# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Payment Type'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)


class ConditionTerms(models.Model):
    _name = 'condition.terms'
    _description = 'Conditions Terms'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)


class ShippingData(models.Model):
    _name = 'shipping.data'
    _description = 'Shipping Data'

    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
