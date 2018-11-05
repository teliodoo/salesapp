# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')

class teli_lead2opportunity_partner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'



    name = fields.Selection([('convert', 'Convert to opportunity')], default='convert')
    partner_ids = fields.Many2many(comodel_name='res.partner', relation='wiz_teli_crm_partnerm2m',
                                    column1='lead_id', column2='partner_id', string='Contacts')
    # credential fields
    username = fields.Char(string='teli Username', required=True)
    account_credit = fields.Char('Initial Account Credit')

    # qualification questions
    monthly_usage = fields.Char(string='Number of monthly messages/minutes?', required=True)
    number_of_dids = fields.Char(string='How many DIDs are in service?', required=True)
    potential = fields.Char(string='What is the potential?', required=True)
    current_service = fields.Char(string='What type of services are they currently using today in their company?', required=True)
    under_contract = fields.Char(string='Are open and available to review and bring on new vendors?', help='Under Contract?', required=True)
    valid_use_case = fields.Boolean(string='Valid Use Case and Overview of their business model?')
    share_rates = fields.Boolean(string='Willing to share target rates?')
    buying_motivation = fields.Selection([
            ('pain', 'Pain?'),
            ('gain', 'Gain?')
        ], 'What\'s the primary motivation for choosing teli?', required=True)
    decision_maker = fields.Selection([
            ('decision_maker', 'End Decision Maker'),
            ('influencer', 'Large Influencer'),
            ('individual', 'Individual')
        ], 'Who is personally overseeing the implementation?', required=True,
        help='Give an overview of the expectations of the next call and the ideal outcome.')
    current_messaging_platform = fields.Char('Current Messaging Platform?',
        help='Is it compatible with XMPP, SMPP, or web services?', required=True)
    interface_preference = fields.Selection([
            ('api', 'API'),
            ('portal', 'Portal')
        ], 'Preferred method of interface?', required=True)
    voice_config = fields.Boolean('Voice configuration uses SIP?', help='No IAX')
    customizations = fields.Text('Any customizations needed?')
    known_issues = fields.Text('Any known issues?')

    @api.model
    def default_get(self, fields):
        """ Set the default values for teli username and initial account credit """
        result = super().default_get(fields)
        lead = self.env['crm.lead'].browse(self._context['active_id'])

        result['username'] = lead.username if lead.username else ''
        result['account_credit'] = lead.account_credit if lead.account_credit else 25

        return result

    @api.multi
    def action_apply(self):
        """ Log qualification answers before moving on. """
        self.ensure_one()

        body = """
            <h4>Initial Qualification Form Results:</h4>
            <dl>
                <dt>Number of monthly messages/minutes?</dt>
                <dd>'{usage}'</dd>
                <dt>How many DIDs are in service?</dt>
                <dd>'{num_dids}'</dd>
                <dt>What is the potential?</dt>
                <dd>'{potential}'</dd>
                <dt>What type of services are they currently using today?</dt>
                <dd>'{services}'</dd>
                <dt>Are open and available to review and bring on new vendors?</dt>
                <dd>'{under_contract}'</dd>
                <dt>Valid use case and overview of their business model?</dt>
                <dd>'{use_case}'</dd>
                <dt>Willing to share target rates?</dt>
                <dd>'{share_rates}'</dd>
                <dt>What's the primary motivation for choosing teli?</dt>
                <dd>'{motivation}'</dd>
                <dt>Who is personally overseeing the implementation?</dt>
                <dd>'{decision_maker}'</dd>
                <dt>What is the current messaging platform?</dt>
                <dd>'{current_platform}'</dd>
                <dt>Preferred method of interface?</dt>
                <dd>'{interface_preference}'</dd>
                <dt>Voice configuration uses SIP?</dt>
                <dd>'{using_sip}'</dd>
                <dt>Any customizations needed?</dt>
                <dd>'{customizations}'</dd>
                <dt>Any known issues?</dt>
                <dd>'{known_issues}'</dd>
            </dl>
            """.format(
                usage=self.monthly_usage,
                num_dids=self.number_of_dids,
                potential=self.potential,
                services=self.current_service,
                under_contract=self.under_contract,
                use_case='yes' if self.valid_use_case else 'no',
                share_rates='yes' if self.share_rates else 'no',
                motivation=self.buying_motivation,
                decision_maker=self.decision_maker,
                current_platform=self.current_messaging_platform,
                interface_preference=self.interface_preference,
                using_sip='yes' if self.voice_config else 'no',
                customizations=self.customizations if self.customizations else 'N/A',
                known_issues=self.known_issues if self.known_issues else 'N/A')

        lead = self.env['crm.lead'].browse(self._context['active_id'])
        lead.username = self.username
        lead.account_credit = self.account_credit
        lead.monthly_usage = self.monthly_usage
        lead.number_of_dids = self.number_of_dids
        lead.potential = self.potential
        lead.current_service = self.current_service
        lead.under_contract = self.under_contract
        lead.valid_use_case = self.valid_use_case
        lead.share_rates = self.share_rates
        lead.buying_motivation = self.buying_motivation
        lead.decision_maker = self.decision_maker
        lead.current_messaging_platform = self.current_messaging_platform
        lead.interface_preference = self.interface_preference
        lead.voice_config = self.voice_config
        lead.customizations = self.customizations
        lead.known_issues = self.known_issues

        _logger.debug("body: %s" % body)
        lead.message_post(body=body, subject="Qualification Answers")
        lead.partner_ids = self.partner_ids
        return super().action_apply()

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
