# -*- coding: utf-8 -*-
from odoo import http
import requests
import json
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel('DEBUG')

class Teliapi(http.Controller):
    """ Teliapi - A controller for making requests to teli's API system.
    """

    _host = 'https://apiv1.teleapi.net'
    _token = '9103c865-dd7d-490c-a05c-fb17f1e57e28' # FIXME This is mines, and needs to go away once I configure the teli_users module
    _create_user_count = 0 # used to increment if username already exists

    @classmethod
    def _call(self, function, params={}, alt_host=None):
        """ _call - a protected method to make calls to the API
            function: a string identifying the API endpoint
            params: a dict of params to pass to the API
        """

        if 'token' not in params:
            # set the token if the calling method left it out
            # FIXME the token needs to be salesperson specific
            params['token'] = self._token

        try:
            host = alt_host if alt_host else self._host
            url = ''.join([host, function])
            _logger.debug('API URL is: %s' % url)
            _logger.debug('data is: %s' % json.dumps(params))
            response = requests.post(url, data=params)
            _logger.debug('response is: %s' % response.content)
            content = response.json()

            _logger.debug(json.dumps(content))

            # TODO work on some error handling
            if response.status_code != 200 or content['code'] != 200:
                _logger.error("[%s] Received non-200 status code" %
                    (response.status_code if response.status_code != 200 else content['code']))
                return content
        except ValueError:
            # according to the requests webpage, a ValueError can occur when
            # attempting to retrieve the json() response content
            # (http://docs.python-requests.org/en/master/user/quickstart/#json-response-content)
            _logger.error("Landed in ValueError land. the raw content is: %s" % response.content)
            return {
                "code": 400,
                "status": "error",
                "data": "%s" % response.content
            }

        return content

    @classmethod
    def create_user(self, params, new_username=None):
        """ create_user - Attempts to sign up
        """

        request_params = {
            'username': params['username'] if params['username'] else
                ("%s-%s" % (params['first_name'], params['last_name'])), # TODO what shall the username be?
            'email': params['email'],
            'first_name': params['first_name'],
            'last_name': params['last_name'],
            'phone': params['phone'],
            'credit': '25', # TODO should this be a custom variable like username?
            # 'token': self._token # FIXME shall use the sales assoc. token
        }

        # optional param, but will probably be needed/supplied by sales
        if params['company_name']:
            request_params['company_name'] = params['company_name']

        if new_username:
            request_params['username'] = new_username

        response = self._call('/sales/create_customer', request_params, 'https://eadmin.teli.co')

        if response['code'] is 400 and response['data'] is 'Username already in use':
            # username error
            self._create_user_count += 1
            response = self.create_customer(params, ''.join([request_params['username'], str(self._create_user_count)])) # TODO need to do something else and rerun

        # bubble up 200s and 500s to the model
        return response

    @classmethod
    def get_user(self):
        """ get_user - Attempts to retrieve the user from teli_api
            returns: a json structure
        """
        return self._call('/user/get')['data']

    @http.route('/teliapi/user/get', type='http', auth='user')
    def get_user_direct(self):
        """ get_user_direct - external testing endpoint for get_user
            returns: a json structure
        """
        return json.dumps(self._call('/user/get')['data'])
