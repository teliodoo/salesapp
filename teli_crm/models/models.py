# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
_logger.setLevel('DEBUG')

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    username = fields.Char('Username', help='Provide the username you want to assign to the lead')
    uuid = fields.Char('Uuid', help='The accounts unique identifier', readonly=True)
    account_credit = fields.Char('Initial Account Credit', default='25')

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
    def handle_partner_assignation(self, action='create', partner_id=False):
        # make call get data
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        if action == 'create':
            # account doesn't exist
            first_name, last_name = self._format_name(self.contact_name)
            params = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': self.mobile if self.mobile else self.phone,
                'email': self.email_from,
                'username': self.username if self.username else "%s.%s" % (first_name, last_name),
                'company_name': self.partner_name,
                'credit': self.account_credit,
                'token': current_user.teli_token,
            }

            create_response = teliapi.create_user(params)

            # Check the response and set a note if the call was successful or not
            if create_response['code'] is not 200:
                self.message_post(content_subtype='plaintext', subject='teli API Warning',
                    body='[WARNING] Encountered an issue attempting to create the new account.')
            else:
                self.message_post(content_subtype='plaintext', subject='teli API Note',
                    body='[SUCCESS] New account was successfully created.')

                # if success, try to grab the uuid and update the oppr/acct
                user_response = teliapi.find_by_username({
                    'token': current_user.teli_token,
                    'username': self.username if self.username else "%s.%s" % (first_name, last_name)
                })
                self.uuid = user_response['auth_token'] if 'auth_token' in user_response else ''

        return super().handle_partner_assignation(action, partner_id)

    @api.multi
    @api.constrains('partner_id')
    def _check_accounts(self):
        """ clean up duplications of the partner_id """

    @api.multi
    @api.constrains('partner_name')
    def _update_teli_username(self):
        """ based on the company name, attempt to set a default username
            NOTE: Should this function search through all partner_names to see
               if it has been used before? Is this really necessary?  How
               does this effect non-new accounts?
        """
        if not self.username:
            self.username = self.partner_name.lower().replace(' ', '.')[:64]
            _logger.debug('username is now: %s' % self.username)

    @api.multi
    @api.onchange('username')
    def _lookup_teli_username(self):
        _logger.debug('type is: %s' % self.type)
        if self.type == 'lead':
            teliapi = self.env['teliapi.teliapi']
            current_user = self.env['res.users'].browse(self.user_id.id)
            _logger.debug('calling find_by_username for: %s' % self.username)
            user_response = teliapi.find_by_username({
                'token': current_user.teli_token,
                'username': self.username
            })

            if 'auth_token' in user_response:
                self.uuid = user_response['auth_token']
                return {
                    'warning': {
                        'title': 'teli Username Check',
                        'message': 'It appears \'%s\' is taken, are you sure you want to do this?' % self.username
                    }
                }
            else:
                self.uuid = ''
        else:
            return {
                'warning': {
                    'title': 'teli Username Check',
                    'message': 'The account has already been created, changing it now is a bad idea.'
                }
            }
