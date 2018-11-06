# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TeliResPartner(models.Model):

    _inherit = 'res.partner'

    _sql_constraints = [
        ('email_partner_user_uniq', 'unique(email)', 'Contact email must be unique!'),
    ]
