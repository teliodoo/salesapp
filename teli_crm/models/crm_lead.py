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
    teli_user_id = fields.Char('teli user id')
    teli_company_name = fields.Char('Company Name')
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

    invoice_term = fields.Selection([
            ('none', 'None'),
            ('30net30', '30 Net 30'),
            ('30net15', '30 Net 15'),
            ('30net10', '30 Net 10'),
            ('30net7', '30 Net 7'),
            ('30net3', '30 Net 3'),
            ('15net15', '15 Net 15'),
            ('7net7', '7 Net 7'),
            ('7net3', '7 Net 3'),
            ('generic', 'Generic'),
            ('teli', 'teli Test Account')
        ], 'Invoice Terms', default='none')
    offnet_dids = fields.Boolean('Enable Offnet DIDs?')
    inbound_channel_limit = fields.Integer('Inbound Channel Limit')
    outbound_channel_limit = fields.Integer('Outbound Channel Limit')
    international_sms = fields.Boolean('Enable International SMS?')
    usf_exempt = fields.Boolean('USF Exempt')
    white_labeling = fields.Boolean('Reselling/White Labeling our Services')

    invoices = fields.One2many(comodel_name='teli.invoice', inverse_name='crm_lead_id', string='Invoice Aggregate')
    products = fields.Many2many('teli.products', 'teli_crm_products_rel', 'crm_lead_id', 'product_id',
                                string="Product Areas of Inital Use")
    gateways = fields.Many2many('teli.gateways', 'teli_crm_gateways_rel', 'crm_lead_id', 'gateway_id',
                                string="Gateways Needed")

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

        # Need to check if the lead was created by the daily cron Job
        user_check = self._call_fetch_user()
        if 'id' in user_check and user_check['id'] == self.teli_user_id and 'auth_token' in user_check and user_check['auth_token'] == self.uuid:
            return False

        # attempt to create the account
        first_name, last_name = self._format_name(self.contact_name)
        params = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': self.mobile if self.mobile else self.phone,
            'email': self.email_from,
            'username': self.username if self.username else "%s.%s" % (first_name, last_name),
            'company_name': self.teli_company_name,
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
            self.teli_user_id = user_response['id'] if 'id' in user_response else ''

    def _call_fetch_user(self):
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)
        _logger.debug('calling find_by_username for: %s' % self.username)
        return teliapi.find_by_username({
            'token': current_user.teli_token,
            'username': self.username
        })

    @api.multi
    def close_dialog(self):
        _logger.debug('hit close_dialog')
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential
        self._call_signup_user()

        return super().close_dialog()

    @api.multi
    def edit_dialog(self):
        _logger.debug('hit edit_dialog')
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential
        self._call_signup_user()

        return super().edit_dialog()

    @api.multi
    def handle_partner_assignation(self, action='create', partner_id=False):
        _logger.debug('hit handle_partner_assignation')
        result = super().handle_partner_assignation(action, partner_id)
        _logger.debug('the parent completed, and now we can create the user on teli')
        self._call_signup_user()

        return result

    @api.onchange('invoice_term')
    def _onchange_invoice_term(self):
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        # If the account was created before the addition of invoice_term, then
        # attempt to get the teli_user_id from the API.
        if not self.teli_user_id:
            result = self._call_fetch_user()
            if 'id' in result:
                self.uuid = result['auth_token'] if 'auth_token' in result else ''
                self.teli_user_id = result['id'] if 'id' in result else ''
            else:
                return {
                    'warning': {
                        'title': 'Unable to Find User',
                        'message': 'Could not set invoice term'
                    }
                }

        response = teliapi.set_invoice_term({
            'user_id': self.teli_user_id,
            'invoice_term': self.invoice_term,
            'token': current_user.teli_token
        })

        if response['status'] is not 'success':
            self.message_post(subject='teli API Warning',
                              body='<h2>[WARNING]</h2><p>%s</p>' % response['data'])

    # --------------------------------------------------------------------------
    #   Constrains
    # --------------------------------------------------------------------------

    @api.multi
    @api.constrains('username')
    def _lookup_teli_username(self):
        user_response = self._call_fetch_user()

        if 'auth_token' in user_response and user_response['auth_token'] != self.uuid:
            raise ValidationError("It appears '%s' is taken.  Try another username." % self.username)

    @api.multi
    @api.constrains('potential')
    def _valid_potential_value(self):
        try:
            temp = int(self.potential)
        except ValueError:
            raise ValidationError('"What is the potential revenue?" must be a numeric value.')


class TeliProducts(models.Model):
    """ Questions:
        - Is there a better way to ensure no duplicate m2m options on reload than a sql constrains?
        - How do I clean up the data in the database?
        - how do/can I define alt string values for m2m options?
    """
    _name = 'teli.products'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class Gateways(models.Model):
    _name = 'teli.gateways'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
