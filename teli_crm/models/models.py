# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def convert_opportunity(self, partner_id, user_ids=False, team_id=False):
        # TODO this should be where we attempt to call the API for account creation
        _logger.debug('Landed in the teli_crm.convert_opportunity method')
        super().convert_opportunity(partner_id, user_ids, team_id)

    @api.multi
    def action_set_won(self):
        _logger.debug('landed in teli_crm.action_set_won')
        super().action_set_won()

    @api.multi
    def action_set_lost(self):
        _logger.debug('OH NO!!! lead has been lost!')
        super().action_set_lost()
#     _name = 'teli_crm.teli_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
