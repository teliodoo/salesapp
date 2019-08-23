# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import datetime
import calendar

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
    ], 'Teli User Status')
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
    use_case_explanation = fields.Text(string='What does the company do?')
    share_rates = fields.Boolean(string='Willing to share target rates?')
    buying_motivation = fields.Char(string='What\'s the primary motivation for choosing teli?')
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
    inbound_channel_limit = fields.Integer('Inbound Channel Limit', default=10)
    outbound_channel_limit = fields.Integer('Outbound Channel Limit', default=10)
    international_sms = fields.Boolean('Enable International SMS?')
    usf_exempt = fields.Boolean('USF Exempt')
    white_labeling = fields.Boolean('Reselling/White Labeling our Services')

    invoices = fields.One2many(comodel_name='teli.invoice', inverse_name='crm_lead_id', string='Invoice Aggregate')
    products = fields.Many2many('teli.products', 'teli_crm_products_rel', 'crm_lead_id', 'product_id',
                                string="Product Areas of Inital Use")
    gateways = fields.Many2many('teli.gateways', 'teli_crm_gateways_rel', 'crm_lead_id', 'gateway_id',
                                string="Gateways Needed")
    month_to_date = fields.Float('Current MTD Total', digits=(13, 2), compute="_calc_month_to_date", store=True)
    prev_mtd = fields.Float('Previous Month Total', digits=(13, 2), compute="_calc_prev_mtd", store=True)
    mtd_delta = fields.Float('MTD Pacing', digits=(13, 2), compute="_calc_mtd_delta", store=True)

    # Social Media Information
    web_technologies = fields.Text('Web Technologies')
    twitter = fields.Char('Twitter Handle', help="place the full URL in the field")
    facebook = fields.Char('Facebook Company Page', help="place the full URL in the field")
    linkedin = fields.Char('LinkedIn Company Page', help="place the full URL in the field")
    twitter_bio = fields.Text('Twitter Bio')
    facebook_notes = fields.Text('Facebook Notes')
    linkedin_notes = fields.Text('LinkedIn Notes')
    linkedin_bio = fields.Text('LinkedIn Bio')

    def _get_current_user(self):
        # originally i was browsing with self.user_id.id, but that caused API changes to potentially show
        # the wrong user made the change.  Going to force the current environment user id going forward.
        current_user = self.env['res.users'].browse(self.env.user.id)
        _logger.debug(current_user.teli_token)
        _logger.debug({
            'env': self.env.user.id,
            'user_id': self.user_id.id
        })

        return current_user

    def _call_signup_user(self):
        # make call get data
        teliapi = self.env['teliapi.teliapi']
        current_user = self._get_current_user()

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

        # If the "enable offnet dids" is checked, then call the api
        if self.offnet_dids:
            result = teliapi.enable_offnet_dids({
                'user_id': self.teli_user_id,
                'token': current_user.teli_token
            })
            if result['code'] is not 200:
                self.message_post(subject='teli API Warning',
                                  body='<h2>[WARNING] Offnet DIDs Enable</h2><p>%s</p>' % result['data'])

        return True

    def _call_fetch_user(self):
        teliapi = self.env['teliapi.teliapi']
        current_user = self._get_current_user()
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

    @api.multi
    def convert_opportunity(self, partner_id, user_ids=False, team_id=False):
        result = super().convert_opportunity(partner_id, user_ids, team_id)

        # copy over social media data to the contact.
        if partner_id:
            customer = self.env['res.partner'].browse(partner_id)
            customer.web_technologies = self.web_technologies if not customer.web_technologies else customer.web_technologies
            customer.twitter = self.twitter
            customer.facebook = self.facebook
            customer.linkedin = self.linkedin
            customer.twitter_bio = self.twitter_bio
            customer.facebook_notes = self.facebook_notes
            customer.linkedin_bio = self.linkedin_bio
            customer.linkedin_notes = self.linkedin_notes

        return result

    # --------------------------------------------------------------------------
    #   Computed
    # --------------------------------------------------------------------------
    @api.one
    @api.depends('month_to_date', 'invoices.total_price')
    def _calc_month_to_date(self):
        _logger.warning('================= _calc_month_to_date ======================')
        first_day_of_month = datetime.date.today()
        first_day_of_month = first_day_of_month.replace(day=1).__str__()
        ia = self.env['teli.invoice'].search([
            ('crm_lead_id', '=', self.id),
            ('create_dt', '>=', first_day_of_month)
        ])

        _logger.debug('working with date: %s' % first_day_of_month)
        _logger.debug('count of teli.invoice: %s' % len(ia))
        temp_value = 0.0
        for agg in ia:
            _logger.debug(' * %s' % agg.total_price)
            temp_value += agg.total_price

        self.month_to_date = temp_value

    @api.one
    @api.depends('prev_mtd', 'invoices.total_price')
    def _calc_prev_mtd(self):
        _logger.warning('================= _calc_prev_mtd ======================')
        first_day_of_month = datetime.date.today().replace(month=datetime.date.today().month-1, day=1).__str__()
        last_day_of_month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).__str__()

        _logger.debug('first DOM: %s' % first_day_of_month)
        _logger.debug('last DOM: %s' % last_day_of_month)

        ia = self.env['teli.invoice'].search([
            ('crm_lead_id', '=', self.id),
            ('create_dt', '>=', first_day_of_month),
            ('create_dt', '<=', last_day_of_month)
        ])

        temp_value = 0.0
        for agg in ia:
            _logger.debug(' * %s' % agg.total_price)
            temp_value += agg.total_price

        self.prev_mtd = temp_value

    @api.one
    @api.depends('month_to_date', 'prev_mtd', 'invoices.total_price')
    def _calc_mtd_delta(self):
        _logger.warning('================= _calc_mtd_delta ======================')
        today = datetime.date.today()
        days_in_current_month = calendar.monthrange(today.year, today.month)[1]
        try:
            self.mtd_delta = ((self.month_to_date / today.day) * days_in_current_month) - self.prev_mtd
            _logger.info('mtd_delta is now: %s' % self.mtd_delta)
        except ZeroDivisionError:
            self.mtd_delta = 0

    # --------------------------------------------------------------------------
    #   Constrains
    # --------------------------------------------------------------------------
    @api.constrains('email_from')
    def _check_contacts_for_email(self):
        _logger.warning('inside email check')
        if not self.email_from:
            return {}

        contacts = self.env['res.partner'].search_count([
            ('email', '=', self.email_from)
        ])

        _logger.info("The current type is %s" % self.type)
        _logger.info("count of contacts with email is %s" % contacts)

        if self.type == 'lead' and contacts > 0:
            raise ValidationError("Unable to create lead/contact as email already exists.  To open a new account with an existing contact, create a new opportunity at the contact level.")

    @api.multi
    @api.constrains('invoice_term')
    def _set_invoice_term(self):
        if not self.teli_user_id:
            return {}

        teliapi = self.env['teliapi.teliapi']
        current_user = self._get_current_user()
        _logger.debug(current_user.teli_token)

        response = teliapi.set_invoice_term({
            'user_id': self.teli_user_id,
            'invoice_term': self.invoice_term,
            'token': current_user.teli_token
        })

        if response['code'] is not 200:
            self.message_post(subject='teli API Warning',
                              body='<h2>[WARNING] Set Invoice Terms</h2><p>%s</p>' % response['data'])

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
            # check to see if potential is not empty first.
            if not self.potential:
                return True

            if self.potential[0] == '$':
                float(self.potential[1:])
            else:
                float(self.potential)

            if self.type == 'opportunity':
                self.planned_revenue = self.potential if self.potential[0] != '$' else self.potential[1:]
        except ValueError:
            raise ValidationError('"What is the potential revenue per month?" must be a numeric value.')

    @api.multi
    @api.constrains('offnet_dids')
    def _enable_offnet_dids(self):
        _logger.debug('offnet_dids is: %s' % self.offnet_dids)

        if self.offnet_dids:
            teliapi = self.env['teliapi.teliapi']
            current_user = self._get_current_user()
            result = teliapi.enable_offnet_dids({
                'user_id': self.teli_user_id,
                'token': current_user.teli_token
            })
            if result['code'] is not 200:
                self.message_post(subject='teli API Warning',
                                  body='<h2>[WARNING] Offnet DIDs Enable</h2><p>%s</p>' % result['data'])

    @api.multi
    @api.constrains('twitter')
    def _twitter_handle_fix(self):
        """ The url widget in Odoo demands a fully qualified URL, so this constrains attempts to enforce that rule
            regardless of the format the user inputs the twitter handle.
            Side Note: we could take this as an opportunity to auto fill bio and/or follower information, but would
            have to apply for their API.
        """
        # first test for non-values or already fully qualified URLs, and returns if passes
        if not self.twitter or self.twitter[0:4] == 'http':
            return True

        # Next check to see if the string starts with "www" (e.g. www.twitter.com/some-company)
        if self.twitter[0:3] == 'www' or self.twitter[0:11] == 'twitter.com':
            self.twitter = 'https://' + self.twitter
        # If the value doesn't start with www, then check for the @ symbol or '/' (the latter probably won't happen)
        elif self.twitter[0] == '@' or self.twitter[0] == '/':
            self.twitter = 'https://twitter.com/' + self.twitter[1:]
        # otherwise, assume the value is the handle and can simply be appended to the twitter domain.
        else:
            self.twitter = 'https://twitter.com/' + self.twitter


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
