# -*- coding: utf-8 -*-

from odoo import models, fields, api

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def convert_opportunity(self, partner_id, user_ids=False, team_id=False):
        # TODO this should be where we attempt to call the API for account creation
        super(partner_id, user_ids, team_id)

#     _name = 'teli_crm.teli_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
