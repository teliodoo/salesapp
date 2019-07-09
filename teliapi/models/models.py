# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.addons.teliapi.controllers.controllers import Teliapi
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')


class teliapi(models.Model):
    _name = "teliapi.teliapi"

    def _format_name(self, name):
        """ _format_name - takes the entire name param and attempts to parse it
            into only first and last names.  This assumes the number is formatted:
            first_name (middle_name or initial) last_name.
            @param name the value of the name field
            @returns first_name, last_name
        """
        if name:
            name_array = name.split()
        else:
            return '', ''

        if len(name_array) == 2:
            return name_array[0], name_array[1]
        else:
            first_name = ' '.join(name_array[:-1])
            last_name = name_array[-1]
            return first_name, last_name

    @api.multi
    def create_user(self, token, name, email, phone, username, credit=25, company_name=False):
        first_name, last_name = self._format_name(name)
        params = {
            'token': token,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'username': username,
            'credit': credit
        }

        if company_name:
            params['company_name'] = company_name

        return Teliapi.create_user(params)

    @api.multi
    def find_by_username(self, params):
        """ find_by_username - searches the teli API for a specific username
            params: a dict containing the following params
             - token
             - username
        """
        return Teliapi.find_by_username(params)

    @api.multi
    def set_invoice_term(self, params):
        """ set_invoice_term - set the invoice term in teli
            params:
             - token
             - user_id
             - invoice_term
        """
        return Teliapi.set_invoice_term(params)

    @api.multi
    def get_user(self):
        """ get_user: tries the user information for a given token.
            Sample Reply: {
               "id":"17740",
               "username":"jd.martin",
               "email":"jd.martin@teli.net",
               "sso_key":"3aa4f834-0030-4176-bdeb-645fa9b1196b",
               "first_name":"JD",
               "last_name":"Martin",
               "phone_number":"3035137389",
               "address":null,
               "city":null,
               "state":null,
               "zip":null,
               "brand":"Teli",
               "domain":"teli622",
               "customer_css":"0",
               "custom_logo":"0",
               "support_phone":null,
               "support_email":null,
               "support_link":null,
               "paypal_address":null,
               "user_status":"active",
               "autofill_enabled":"0",
               "autofill_amount":"20.00",
               "inbound_channels":"10",
               "outbound_channels":"1",
               "max_international":"190.000000",
               "sms_post_url":"https://api.your.domain.com/api/sms",
               "web_hook_url":"https://api.your.domain.com/api/hook",
               "did_sbc":"208.103.145.20"
            }
        """
        get_user_response = Teliapi.get_user()

        return get_user_response

    @api.multi
    def enable_offnet_dids(self, params):
        """ enable_offnet_dids - tries to turn on offnet dids for a given teli_user_id
            params:
             - user_id: the teli user_id
             - token: user's token
        """
        return Teliapi.enable_offnet_dids(params)
