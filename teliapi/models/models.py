# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.teliapi.controllers.controllers import Teliapi
import logging

_logger = logging.getLogger(__name__)

class teliapi(models.Model):
    _name = "teliapi.teliapi"

    @api.multi
    def create_user(self):
        response = Teliapi.create_user()
        # _logger.warning('response: ' + str(response.__dict__))

        # do some magic if needed
        # params.id = response.id
        # params.name = response['first_name'] + ' ' + response['last_name']
        # params.email = response['email']
        # params.phone = response['phone_number']
        # _logger.warning('from create_user: ' + str(params.__dict__))

        return response

    @api.multi
    def get_user(self):
        get_user_response = Teliapi.get_user()

        return get_user_response
