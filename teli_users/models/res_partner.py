# -*- coding: utf-8 -*-

from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')


class TeliResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('email_partner_user_uniq', 'unique(email)', 'Contact email must be unique!'),
    ]

    # Social Media Information
    web_technologies = fields.Text('Web Technologies')
    twitter = fields.Char('Twitter Handle', help="place the full URL in the field")
    facebook = fields.Char('Facebook Company Page', help="place the full URL in the field")
    linkedin = fields.Char('LinkedIn Company Page', help="place the full URL in the field")
    twitter_bio = fields.Text('Twitter Bio')
    facebook_notes = fields.Text('Facebook Notes')
    linkedin_notes = fields.Text('LinkedIn Notes')
    linkedin_bio = fields.Text('LinkedIn Bio')

    property_account_payable_id = fields.Many2one('account.account', required=False)
    property_account_receivable_id = fields.Many2one('account.account', required=False)

    # ==================== COMPUTED ================================================================================
    @api.multi
    def _compute_opportunity_count(self):
        for partner in self:
            # the opportunity count should counts the opportunities of this company and all its contacts
            operator = 'child_of' if partner.is_company else '='
            partner.opportunity_count = self.env['crm.lead'].search_count(
                [('partner_id', operator, partner.id), ('type', '=', 'opportunity')])
            partner.opportunity_count += self.env['crm.lead'].search_count(
                [('partner_ids', 'in', partner.id), ('type', '=', 'opportunity')])

    # ==================== CONSTRAINS ================================================================================
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
