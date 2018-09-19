# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)
_logger.setLevel('DEBUG')

class teli_lead2opportunity_partner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    # qualification questions
    monthly_usage = fields.Char(string='Number of monthly messages/minutes?', required=True)
    number_of_dids = fields.Char(string='How many DIDs are in service?', required=True)
    potential = fields.Char(string='What is the potential?', required=True)

    current_service = fields.Char(string='What type of services are they currently using today in their company?', required=True)

    under_contract = fields.Char(string='Are open and available to review and bring on new vendors?', help='Under Contract?', required=True)

    valid_use_case = fields.Boolean(string='Valid Use Case and Overview of their business model', required=True)

    share_rates = fields.Boolean(string='Willing to share target rates?', required=True)
