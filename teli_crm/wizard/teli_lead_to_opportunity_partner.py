# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')

class teli_lead2opportunity_partner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

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
                customizations=self.customizations,
                known_issues=self.known_issues)

        _logger.debug("body: %s" % body)
        leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
        leads[0].message_post(body=body, subject="Qualification Answers")

        return super().action_apply()
