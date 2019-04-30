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
    teli_lead_status = fields.Selection([
        ('open', 'Open'),
        ('qualifying', 'Qualifying'),
        ('recycled', 'Recycled'),
        ('unqualified', 'Unqualified'),
        ('dead', 'Dead')
    ], 'Lead Status')
    teli_user_id = fields.Char('teli user id')
    teli_company_name = fields.Char('Company Name')
    username = fields.Char('Username', help='Provide the username you want to assign to the lead')
    uuid = fields.Char('Uuid', help='The accounts unique identifier', readonly=True)
    account_credit = fields.Char('Initial Account Credit', default='25')
    account_status = fields.Selection([
        ('active', 'Active'),
        ('inactive-disabled', 'Disabled'),
        ('inactive-no-funds-soft', 'No Funds - Soft Inactive'),
        ('inactive-no-funds-hard', 'No Funds - Hard Inactive'),
        ('inactive-fraud', 'Inactive Fraud'),
        ('pending-approval', 'Pending Approval')
    ], 'Account Status')
    skip_constrains_test = True
    # teli_revenue = fields.Char('Revenue')
    # teli_usage = fields.Char('Usage')

    # qualification questions
    monthly_usage = fields.Char(string='Number of monthly messages/minutes?')
    number_of_dids = fields.Char(string='How many DIDs are in service?')
    potential = fields.Char(string='What is the potential revenue per month?')
    current_service = fields.Char(string='What type of services are they currently using today in their company?')
    under_contract = fields.Char(string='Are open and available to review and bring on new vendors?',
                                 help='Under Contract?')
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
    # invoice_agg = fields.One2many(comodel_name='teli.invoice.aggregate', inverse_name='crm_lead_id',
    #                               string="Invoice Aggregate")
    products = fields.Many2many('teli.products', 'teli_crm_products_rel', 'crm_lead_id', 'product_id',
                                string="Product Areas of Inital Use")
    gateways = fields.Many2many('teli.gateways', 'teli_crm_gateways_rel', 'crm_lead_id', 'gateway_id',
                                string="Gateways Needed")

    def _call_signup_user(self):
        # make call get data
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        create_response = teliapi.create_user(
            current_user.teli_token,
            self.contact_name,
            self.email_from,
            self.mobile if self.mobile else self.phone,
            self.username,
            self.account_credit,
            self.teli_company_name
        )

        # Check the response and set a note if the call was successful or not
        if create_response['code'] is not 200:
            self.message_post(content_subtype='plaintext', subject='teli API Warning',
                              body='[WARNING] Received the following error from teli: %s' % create_response['data'])
            return False

        self.message_post(content_subtype='plaintext', subject='teli API Note',
                          body='[SUCCESS] New account was successfully created.')

        # if success, try to grab the uuid and update the oppr/acct
        user_response = teliapi.find_by_username({
            'token': current_user.teli_token,
            'username': self.username
        })
        self.uuid = user_response['auth_token'] if 'auth_token' in user_response else ''
        self.teli_user_id = user_response['id'] if 'id' in user_response else ''
        return True

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
        self.skip_constrains_test = False

        if not self._call_signup_user():
            raise ValidationError("An error occurred while attempting to create the account.")
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential

        result = super().close_dialog()
        self.skip_constrains_test = True
        return result

    @api.multi
    def edit_dialog(self):
        _logger.debug('hit edit_dialog')
        self.skip_constrains_test = False

        if not self._call_signup_user():
            raise ValidationError("An error occurred while attempting to create the account.")
        self.planned_revenue = self.planned_revenue if self.planned_revenue else self.potential

        result = super().edit_dialog()
        self.skip_constrains_test = True
        return result

    # --------------------------------------------------------------------------
    #   Constrains
    # --------------------------------------------------------------------------
    @api.multi
    @api.constrains('invoice_term')
    def _set_invoice_term(self):
        if not self.teli_user_id:
            return {}

        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        response = teliapi.set_invoice_term({
            'user_id': self.teli_user_id,
            'invoice_term': self.invoice_term,
            'token': current_user.teli_token
        })

        if response['code'] is not 200:
            self.message_post(subject='teli API Warning',
                              body='<h2>[WARNING]</h2><p>%s</p>' % response['data'])

    @api.multi
    @api.constrains('username')
    def _lookup_teli_username(self):
        if self.skip_constrains_test:
            _logger.warn('Skipping username constraint test')
            return True

        user_response = self._call_fetch_user()

        # Check to see if we get a "User not found" response from the teli API
        # elif the username requested returns a valid user object, then that account exists and a new username is needed
        if 'code' in user_response and user_response['code'] != 200 and user_response['data'] != 'User not found':
            raise ValidationError("An error occurred: %s" % user_response['data'])
        elif all(k in user_response for k in ("id", "username", "email", "auth_token")):
            raise ValidationError("It appears '%s' is taken.  Try another username." % self.username)

    @api.multi
    @api.constrains('potential')
    def _valid_potential_value(self):
        try:
            int(self.potential)
        except ValueError:
            raise ValidationError('"What is the potential revenue per month?" must be a numeric value.')


class TeliProducts(models.Model):
    _name = 'teli.products'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]


class Gateways(models.Model):
    _name = 'teli.gateways'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
