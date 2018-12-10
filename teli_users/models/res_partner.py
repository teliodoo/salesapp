# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TeliResPartner(models.Model):

    _inherit = 'res.partner'

    _sql_constraints = [
        ('email_partner_user_uniq', 'unique(email)', 'Contact email must be unique!'),
    ]

    @api.multi
    def _compute_opportunity_count(self):
        for partner in self:
            operator = 'child_of' if partner.is_company else '='  # the opportunity count should counts the opportunities of this company and all its contacts
            partner.opportunity_count = self.env['crm.lead'].search_count([('partner_id', operator, partner.id), ('type', '=', 'opportunity')])
            partner.opportunity_count += self.env['crm.lead'].search_count([('partner_ids', 'in', partner.id), ('type', '=', 'opportunity')])
