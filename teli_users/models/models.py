# -*- coding: utf-8 -*-

from odoo import models, fields, api

class teli_users(models.Model):
    _inherit = 'res.users'

    teli_token = fields.Char(string='Sales Associate Token',
        help="This field shall be your Teli Token for making requests to the API.")
