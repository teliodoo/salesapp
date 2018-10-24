# -*- coding: utf-8 -*-

from odoo import models, fields, api

class teli_users(models.Model):
    _inherit = 'res.users'

    """ teli_token is the token used to access the admin API.  This requires a manual
        step to activate a new sales associate.  A dev needs to run the following
        SQL statement.

        INSERT INTO
            sessions (admin_user_id, token, api_never_kill)
        VALUES
            (<admin id>, <generated uuid>, 'yes')
    """
    teli_token = fields.Char(string='Sales Associate Token',
        help="This field shall be your Teli Token for making requests to the API.")
