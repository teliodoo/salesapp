# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    partner_ids = fields.Many2many(comodel_name='res.partner', relation='teli_crm_partnerm2m',
                                    column1='lead_id', column2='partner_id', string='Contacts')
    username = fields.Char('Username', help='Provide the username you want to assign to the lead')
    uuid = fields.Char('Uuid', help='The accounts unique identifier', readonly=True)
    account_credit = fields.Char('Initial Account Credit', default='25')

    # qualification questions
    monthly_usage = fields.Char(string='Number of monthly messages/minutes?')
    number_of_dids = fields.Char(string='How many DIDs are in service?')
    potential = fields.Char(string='What is the potential revenue?')
    current_service = fields.Char(string='What type of services are they currently using today in their company?')
    under_contract = fields.Char(string='Are open and available to review and bring on new vendors?', help='Under Contract?')
    valid_use_case = fields.Boolean(string='Valid Use Case and Overview of their business model?')
    share_rates = fields.Boolean(string='Willing to share target rates?')
    buying_motivation = fields.Selection([
            ('pain', 'Pain'),
            ('gain', 'Gain')
        ], 'What\'s the primary motivation for choosing teli?')
    decision_maker = fields.Selection([
            ('decision_maker', 'End Decision Maker'),
            ('influencer', 'Large Influencer'),
            ('individual', 'Individual')
        ], 'Who is personally overseeing the implementation?',
        help='Give an overview of the expectations of the next call and the ideal outcome.')
    current_messaging_platform = fields.Char('Current Messaging Platform?',
        help='Is it compatible with XMPP, SMPP, or web services?')
    interface_preference = fields.Selection([
            ('api', 'API'),
            ('portal', 'Portal')
        ], 'Preferred method of interface?')
    voice_config = fields.Boolean('Voice configuration uses SIP?', help='No IAX')
    customizations = fields.Text('Any customizations needed?')
    known_issues = fields.Text('Any known issues?')

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

    def _call_signup_user(self):
        # make call get data
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        # attempt to create the account
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
                body='[WARNING] Received the following error from teli: %s' % create_response['data'])
        else:
            self.message_post(content_subtype='plaintext', subject='teli API Note',
                body='[SUCCESS] New account was successfully created.')

            # if success, try to grab the uuid and update the oppr/acct
            user_response = teliapi.find_by_username({
                'token': current_user.teli_token,
                'username': self.username if self.username else "%s.%s" % (first_name, last_name)
            })
            self.uuid = user_response['auth_token'] if 'auth_token' in user_response else ''

    @api.multi
    def close_dialog(self):
        _logger.debug('hit close_dialog')
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential
        _call_signup_user()

        return super().close_dialog()

    @api.multi
    def edit_dialog(self):
        _logger.debug('hit edit_dialog')
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential
        _call_signup_user()

        return super().edit_dialog()

    @api.multi
    def handle_partner_assignation(self, action='create', partner_id=False):
        _logger.debug('hit handle_partner_assignation')
        _call_signup_user()

        return super().handle_partner_assignation(action, partner_id)

    # --------------------------------------------------------------------------
    #   Constrains
    # --------------------------------------------------------------------------

    @api.multi
    @api.constrains('username')
    def _lookup_teli_username(self):
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)
        _logger.debug('calling find_by_username for: %s' % self.username)
        user_response = teliapi.find_by_username({
            'token': current_user.teli_token,
            'username': self.username
        })

        if 'auth_token' in user_response:
            raise ValidationError("It appears '%s' is taken.  Try another username." % self.username)

    @api.multi
    @api.constrains('potential')
    def _valid_potential_value(self):
        try:
            temp = int(self.potential)
        except ValueError:
            raise ValidationError('"What is the potential revenue?" must be a numeric value.')
