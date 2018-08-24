# -*- coding: utf-8 -*-
from odoo import http
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class Teliapi(http.Controller):
    """ Teliapi - A controller for making requests to teli's API system.
    """

    _host = 'https://apiv1.teleapi.net'
    _token = 'ff8e8369-a767-4b62-b733-f910028baefd' # TODO This is mines.  Need to update

    def _call(self, function, params={}):
        """ _call - a protected method to make calls to the API
            function: a string identifying the API endpoint
            params: a dict of params to pass to the API
        """

        if 'token' not in params:
            # set the token if the calling method left it out
            params['token'] = self._token

        try:
            response = requests.post(self._host + function, data=params)
            content = response.json()

            _logger.debug(json.dumps(content))

            # TODO work on some error handling
            if response.status_code != 200 or content['code'] != 200:
                _logger.error("[%s] Received non-200 status code" %
                    (response.status_code if response.status_code != 200 else content['code']))
                return content
        except ValueError:
            _logger.error("Landed in ValueError land.")
            return {
                "code": 400,
                "status": "error",
                "data": "Caught a ValueError while attempting to call '%s'" % function
            }

        return content['data']

    @classmethod
    def create_user(self):
        """ create_user - Attempts to sign up
        """
        params = {
            "token": self._token,
            "username": "something",
            "email": params and params.email or False,
            "first_name": params.first_name,
            "last_name": params.last_name,
            "phone": params and params.phone or False,
            "company_name": "Big Bucks",
            "company_title": "CEO",
            "aid": "",
            "promo": "",
            "teli_contact": params.teli_contact
        }

        content = self._call('/signup', params)

        return content

    @classmethod
    def get_user(self):
        """ get_user - Attempts to retrieve the user from teli_api
            returns: a json structure
        """
        return self._call('/user/get')

    @http.route('/teliapi/user/get', type='http', auth='user')
    def get_user_direct(self):
        """ get_user_direct - external testing endpoint for get_user
            returns: a json structure
        """
        return json.dumps(self._call('/user/get'))
