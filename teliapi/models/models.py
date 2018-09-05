# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.teliapi.controllers.controllers import Teliapi
import logging

_logger = logging.getLogger(__name__)

class teliapi(models.Model):
    _name = "teliapi.teliapi"

    @api.multi
    def create_user(self, params):
        """ create_user - attempts to call the user signup API
            params: A dict containing the following params
                - token
                - first_name
                - last_name
                - email
                - phone
                - username (optional)
                - company_name (optional)
        """

        response = Teliapi.create_user(params)

        return response

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
