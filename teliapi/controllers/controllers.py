# -*- coding: utf-8 -*-
from odoo import http
import requests
import json
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')

class Teliapi(http.Controller):
    """ Teliapi - A controller for making requests to teli's API system.
    """

    _host = 'https://eadmin.teli.co'
    _create_user_count = 0 # used to increment if username already exists

    @classmethod
    def _call(self, function, params={}, alt_host=None):
        """ _call - a protected method to make calls to the API
            function: a string identifying the API endpoint
            params: a dict of params to pass to the API
        """

        try:
            host = alt_host if alt_host else self._host
            url = ''.join([host, function])
            _logger.debug('API URL is: %s' % url)
            _logger.debug('data is: %s' % json.dumps(params))
            response = requests.post(url, data=params)
            _logger.debug('response is: %s' % response.content)
            content = response.json()

            _logger.debug(json.dumps(content))

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
            'username': params['username'] if 'username' in params else
                ("%s-%s" % (params['first_name'], params['last_name'])), # TODO what shall the username be?
            'email': params['email'],
            'first_name': params['first_name'],
            'last_name': params['last_name'],
            'phone': params['phone'],
            'credit': params['credit'],
            'token': params['token'],
        }

        # debugging the return
        # return {
        #     "code": 200,
        #     "status": "success",
        #     "data": "[DEBUG] An account was not created"
        # }

        for key, value in request_params.items():
            _logger.debug("%s => %s" % (key, value))

        # optional param, but will probably be needed/supplied by sales
        if params['company_name']:
            request_params['company_name'] = params['company_name']

        if new_username:
            request_params['username'] = new_username

        response = self._call('/sales/create_customer', request_params)

        if response['code'] is 400 and response['data'] is 'Username already in use':
            # FIXME this is untested, and shouldn't be necessary because the associate can set the username in the CRM.
            # username error
            self._create_user_count += 1
            response = self.create_customer(params, ''.join([request_params['username'], str(self._create_user_count)])) # TODO need to do something else and rerun

        # bubble up 200s and 500s to the model
        return response

    @classmethod
    def find_by_username(self, params, offset=0):
        """ find_by_username
        """
        response = self._call('/user/info/username', {
            'username': params['username'],
            'user_type': 'master',
            'token': params['token']
        })

        # check the response for no data returned
        if response['code'] is not 200:
            _logger.warning('[ERROR][%s] received an error: %s' % (response['code'], response['data']))
            return {}

        if len(response['data']) is 0:
            _logger.warning('No results found')
            return {}

        # search the data for the recently created user account
        for user in response['data']:
            _logger.debug('checking user: %s' % user['username'])
            if params['username'] == user['username']:
                _logger.debug('Found the right user!!!')
                return user

        _logger.warning('Couldn\'t find the correct user...')
        return {}

    @classmethod
    def get_user(self):
        """ get_user - Attempts to retrieve the user from teli_api
            returns: a json structure
        """
        return self._call('/user/get', alt_host='https://apiv1.teleapi.net')['data']

    @http.route('/teliapi/user/get', type='http', auth='user')
    def get_user_direct(self):
        """ get_user_direct - external testing endpoint for get_user
            returns: a json structure
        """
        return json.dumps(self._call('/user/get', alt_host='https://apiv1.teleapi.net')['data'])
