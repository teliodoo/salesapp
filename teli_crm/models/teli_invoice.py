# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')


class TeliInvoice(models.Model):
    _name = 'teli.invoice'

    crm_lead_id = fields.Many2one('crm.lead', string='Account', index=True)

    # Channel Groups ----------------------------------------------------------------------
    channel_groups_qty = fields.Integer('Channel Groups Quantity', default=0)
    channel_groups_price = fields.Float('Channel Groups Price', digits=(13, 6), default=0.0)
    channel_groups_amount = fields.Float('Channel Groups Amount', compute='_compute_cg_amount')

    @api.one
    @api.depends('channel_groups_qty', 'channel_groups_price')
    def _compute_cg_amount(self):
        self.channel_groups_amount = self.channel_groups_qty * self.channel_groups_price

    # Local Numbers ----------------------------------------------------------------------
    local_numbers = fields.Integer('Local Numbers', default=0)
    local_numbers_price = fields.Float('Local Numbers Price', digits=(13, 6), default=0.0)
    local_numbers_amount = fields.Float('Local Numbers Amount', compute='_compute_ln_amount')

    @api.one
    @api.depends('local_numbers', 'local_numbers_price')
    def _compute_ln_amount(self):
        self.local_numbers_amount = self.local_numbers * self.local_numbers_price

    # Tollfree Numbers ----------------------------------------------------------------------
    tollfree_numbers = fields.Integer('Tollfree Numbers', default=0)
    tollfree_numbers_price = fields.Float('Tollfree Numbers Price', digits=(13, 6), default=0.0)
    tollfree_numbers_amount = fields.Float('Tollfree Numbers Amount', compute='_compute_tf_amount')

    @api.one
    @api.depends('tollfree_numbers', 'tollfree_numbers_price')
    def _compute_tf_amount(self):
        self.tollfree_numbers_amount = self.tollfree_numbers * self.tollfree_numbers_price

    # Offnet Numbers ----------------------------------------------------------------------
    offnet_numbers = fields.Integer('Offnet Numbers', default=0)
    offnet_numbers_price = fields.Float('Offnet Numbers Price', digits=(13, 6), default=0.0)
    offnet_numbers_amount = fields.Float('Offnet Numbers Amount', compute='_compute_onn_amount')

    @api.one
    @api.depends('offnet_numbers', 'offnet_numbers_price')
    def _compute_onn_amount(self):
        self.offnet_numbers_amount = self.offnet_numbers * self.offnet_numbers_price

    # International Numbers ----------------------------------------------------------------------
    international_numbers = fields.Integer('International Numbers', default=0)
    international_numbers_price = fields.Float('International Numbers Price', digits=(13, 6), default=0.0)
    international_numbers_amount = fields.Float('International Numbers Amount', compute='_compute_intl_amount')

    @api.one
    @api.depends('international_numbers', 'international_numbers_price')
    def _compute_intl_amount(self):
        self.international_numbers_amount = self.international_numbers * self.international_numbers_price

    # LNP Requests ----------------------------------------------------------------------
    lnp_requests = fields.Integer('LNP Requests', default=0)
    lnp_requests_price = fields.Float('LNP Requests Price', digits=(13, 6), default=0.0)
    lnp_requests_amount = fields.Float('LNP Requests Amount', compute='_compute_lnp_amount')

    @api.one
    @api.depends('lnp_requests', 'lnp_requests_price')
    def _compute_lnp_amount(self):
        self.lnp_requests_amount = self.lnp_requests * self.lnp_requests_price

    # Minutes Inbound ----------------------------------------------------------------------
    minutes_inbound = fields.Integer('Minutes Inbound', default=0)
    minutes_inbound_price = fields.Float('Minutes Inbound Price', digits=(13, 6), default=0.0)
    minutes_inbound_amount = fields.Float('Minutes Inbound Amount', compute='_compute_min_in_amount')

    @api.one
    @api.depends('minutes_inbound', 'minutes_inbound_price')
    def _compute_min_in_amount(self):
        self.minutes_inbound_amount = self.minutes_inbound * self.minutes_inbound_price

    # Minutes Outbound ----------------------------------------------------------------------
    minutes_outbound = fields.Integer('Minutes Outbound', default=0)
    minutes_outbound_price = fields.Float('Minutes Outbound Price', digits=(13, 6), default=0.0)
    minutes_outbound_amount = fields.Float('Minutes Outbound Amount', compute='_compute_min_out_amount')

    @api.one
    @api.depends('minutes_outbound', 'minutes_outbound_price')
    def _compute_min_out_amount(self):
        self.minutes_outbound_amount = self.minutes_outbound * self.minutes_outbound_price

    # SIP/Nav Minutes Outbound ----------------------------------------------------------------------
    sipnav_minutes_outbound = fields.Integer('SIPNav Minutes Outbound', default=0)
    sipnav_minutes_outbound_price = fields.Float('SIPNav Minutes Outbound Price', digits=(13, 6), default=0.0)
    sipnav_minutes_outbound_amount = fields.Float('SIPNav Minutes Outbound Amount', compute='_compute_sipnav_amount')

    @api.one
    @api.depends('sipnav_minutes_outbound', 'sipnav_minutes_outbound_price')
    def _compute_sipnav_amount(self):
        self.sipnav_minutes_outbound_amount = self.sipnav_minutes_outbound * self.sipnav_minutes_outbound_price

    # Local SMS Inbound ----------------------------------------------------------------------
    local_sms_in = fields.Integer('Local SMS Inbound', default=0)
    local_sms_in_price = fields.Float('Local SMS Inbound Price', digits=(13, 6), default=0.0)
    local_sms_in_amount = fields.Float('Local SMS Inbound Amount', compute='_compute_local_sms_in_amount')

    @api.one
    @api.depends('local_sms_in', 'local_sms_in_price')
    def _compute_local_sms_in_amount(self):
        self.local_sms_in_amount = self.local_sms_in * self.local_sms_in_price

    # Local SMS Outbound ----------------------------------------------------------------------
    local_sms_out = fields.Integer('Local SMS Outbound', default=0)
    local_sms_out_price = fields.Float('Local SMS Outbound Price', digits=(13, 6), default=0.0)
    local_sms_out_amount = fields.Float('Local SMS Outbound Amount', compute='_compute_local_sms_out_amount')

    @api.one
    @api.depends('local_sms_out', 'local_sms_out_price')
    def _compute_local_sms_out_amount(self):
        self.local_sms_out_amount = self.local_sms_out * self.local_sms_out_price

    # Local MMS Inbound ----------------------------------------------------------------------
    local_mms_in = fields.Integer('Local MMS Inbound', default=0)
    local_mms_in_price = fields.Float('Local MMS Inbound Price', digits=(13, 6), default=0.0)
    local_mms_in_amount = fields.Float('Local MMS Inbound Amount', compute='_compute_local_mms_in_amount')

    @api.one
    @api.depends('local_mms_in', 'local_mms_in_price')
    def _compute_local_mms_in_amount(self):
        self.local_mms_in_amount = self.local_mms_in * self.local_mms_in_price

    # Local MMS Outbound ----------------------------------------------------------------------
    local_mms_out = fields.Integer('Local MMS Outbound', default=0)
    local_mms_out_price = fields.Float('Local MMS Outbound Price', digits=(13, 6), default=0.0)
    local_mms_out_amount = fields.Float('Local MMS Outbound Amount', compute='_compute_local_mms_out_amount')

    @api.one
    @api.depends('local_mms_out', 'local_mms_out_price')
    def _compute_local_mms_out_amount(self):
        self.local_mms_out_amount = self.local_mms_out * self.local_mms_out_price

    # Shortcode SMS Inbound ----------------------------------------------------------------------
    sc_sms_in = fields.Integer('Shortcode SMS Inbound', default=0)
    sc_sms_in_price = fields.Float('Shortcode SMS Inbound Price', digits=(13, 6), default=0.0)
    sc_sms_in_amount = fields.Float('Shortcode SMS Inbound Amount', compute='_compute_sc_sms_in_amount')

    @api.one
    @api.depends('sc_sms_in', 'sc_sms_in_price')
    def _compute_sc_sms_in_amount(self):
        self.sc_sms_in_amount = self.sc_sms_in * self.sc_sms_in_price

    # Shortcode SMS Outbound ----------------------------------------------------------------------
    sc_sms_out = fields.Integer('Shortcode SMS Outbound', default=0)
    sc_sms_out_price = fields.Float('Shortcode SMS Outbound Price', digits=(13, 6), default=0.0)
    sc_sms_out_amount = fields.Float('Shortcode SMS Outbound Amount', compute='_compute_sc_sms_out_amount')

    @api.one
    @api.depends('sc_sms_out', 'sc_sms_out_price')
    def _compute_sc_sms_out_amount(self):
        self.sc_sms_out_amount = self.sc_sms_out * self.sc_sms_out_price

    # Shortcode MMS Inbound ----------------------------------------------------------------------
    sc_mms_in = fields.Integer('Shortcode MMS Inbound', default=0)
    sc_mms_in_price = fields.Float('Shortcode MMS Inbound Price', digits=(13, 6), default=0.0)
    sc_mms_in_amount = fields.Float('Shortcode MMS Inbound Amount', compute='_compute_sc_mms_in_amount')

    @api.one
    @api.depends('sc_mms_in', 'sc_mms_in_price')
    def _compute_sc_mms_in_amount(self):
        self.sc_mms_in_amount = self.sc_mms_in * self.sc_mms_in_price

    # Shortcode MMS Outbound ----------------------------------------------------------------------
    sc_mms_out = fields.Integer('Shortcode MMS Outbound', default=0)
    sc_mms_out_price = fields.Float('Shortcode MMS Outbound Price', digits=(13, 6), default=0.0)
    sc_mms_out_amount = fields.Float('Shortcode MMS Outbound Amount', compute='_compute_sc_mms_out_amount')

    @api.one
    @api.depends('sc_mms_out', 'sc_mms_out_price')
    def _compute_sc_mms_out_amount(self):
        self.sc_mms_out_amount = self.sc_mms_out * self.sc_mms_out_price

    # Tollfree SMS Inbound ----------------------------------------------------------------------
    tf_sms_in = fields.Integer('Tollfree SMS Inbound', default=0)
    tf_sms_in_price = fields.Float('Tollfree SMS Inbound Price', digits=(13, 6), default=0.0)
    tf_sms_in_amount = fields.Float('Tollfree SMS Inbound Amount', compute='_compute_tf_sms_in_amount')

    @api.one
    @api.depends('tf_sms_in', 'tf_sms_in_price')
    def _compute_tf_sms_in_amount(self):
        self.tf_sms_in_amount = self.tf_sms_in * self.tf_sms_in_price

    # Tollfree SMS Outbound ----------------------------------------------------------------------
    tf_sms_out = fields.Integer('Tollfree SMS Outbound', default=0)
    tf_sms_out_price = fields.Float('Tollfree SMS Outbound Price', digits=(13, 6), default=0.0)
    tf_sms_out_amount = fields.Float('Tollfree SMS Outbound Amount', compute='_compute_tf_sms_out_amount')

    @api.one
    @api.depends('tf_sms_out', 'tf_sms_out_price')
    def _compute_tf_sms_out_amount(self):
        self.tf_sms_out_amount = self.tf_sms_out * self.tf_sms_out_price

    # Tollfree MMS Inbound ----------------------------------------------------------------------
    tf_mms_in = fields.Integer('Tollfree MMS Inbound', default=0)
    tf_mms_in_price = fields.Float('Tollfree MMS Inbound Price', digits=(13, 6), default=0.0)
    tf_mms_in_amount = fields.Float('Tollfree MMS Inbound Amount', compute='_compute_tf_mms_in_amount')

    @api.one
    @api.depends('tf_mms_in', 'tf_mms_in_price')
    def _compute_tf_mms_in_amount(self):
        self.tf_mms_in_amount = self.tf_mms_in * self.tf_mms_in_price

    # Tollfree MMS Outbound ----------------------------------------------------------------------
    tf_mms_out = fields.Integer('Tollfree MMS Outbound', default=0)
    tf_mms_out_price = fields.Float('Tollfree MMS Outbound Price', digits=(13, 6), default=0.0)
    tf_mms_out_amount = fields.Float('Tollfree MMS Outbound Amount', compute='_compute_tf_mms_out_amount')

    @api.one
    @api.depends('tf_mms_out', 'tf_mms_out_price')
    def _compute_tf_mms_out_amount(self):
        self.tf_mms_out_amount = self.tf_mms_out * self.tf_mms_out_price

    # International SMS Inbound ----------------------------------------------------------------------
    intl_sms_in = fields.Integer('International SMS Inbound', default=0)
    intl_sms_in_price = fields.Float('International SMS Inbound Price', digits=(13, 6), default=0.0)
    intl_sms_in_amount = fields.Float('International SMS Inbound Amount', compute='_compute_intl_sms_in_amount')

    @api.one
    @api.depends('intl_sms_in', 'intl_sms_in_price')
    def _compute_intl_sms_in_amount(self):
        self.intl_sms_in_amount = self.intl_sms_in * self.intl_sms_in_price

    # International SMS Outbound ----------------------------------------------------------------------
    intl_sms_out = fields.Integer('International SMS Outbound', default=0)
    intl_sms_out_price = fields.Float('International SMS Outbound Price', digits=(13, 6), default=0.0)
    intl_sms_out_amount = fields.Float('International SMS Outbound Amount', compute='_compute_intl_sms_out_amount')

    @api.one
    @api.depends('intl_sms_out', 'intl_sms_out_price')
    def _compute_intl_sms_out_amount(self):
        self.intl_sms_out_amount = self.intl_sms_out * self.intl_sms_out_price

    # International MMS Inbound ----------------------------------------------------------------------
    intl_mms_in = fields.Integer('International MMS Inbound', default=0)
    intl_mms_in_price = fields.Float('International MMS Inbound Price', digits=(13, 6), default=0.0)
    intl_mms_in_amount = fields.Float('International MMS Inbound Amount', compute='_compute_intl_mms_in_amount')

    @api.one
    @api.depends('intl_mms_in', 'intl_mms_in_price')
    def _compute_intl_mms_in_amount(self):
        self.intl_mms_in_amount = self.intl_mms_in * self.intl_mms_in_price

    # International MMS Outbound ----------------------------------------------------------------------
    intl_mms_out = fields.Integer('International MMS Outbound', default=0)
    intl_mms_out_price = fields.Float('International MMS Outbound Price', digits=(13, 6), default=0.0)
    intl_mms_out_amount = fields.Float('International MMS Outbound Amount', compute='_compute_intl_mms_out_amount')

    @api.one
    @api.depends('intl_mms_out', 'intl_mms_out_price')
    def _compute_intl_mms_out_amount(self):
        self.intl_mms_out_amount = self.intl_mms_out * self.intl_mms_out_price

    # Emergency 911 Service ----------------------------------------------------------------------
    e911 = fields.Integer('911 Service', default=0)
    e911_price = fields.Float('911 Service Price', digits=(13, 6), default=0.0)
    e911_amount = fields.Float('911 Service Amount', compute='_compute_e911_amount')

    @api.one
    @api.depends('e911', 'e911_price')
    def _compute_e911_amount(self):
        self.e911_amount = self.e911 * self.e911_price

    # Summary Information -----------------------------------------------------------------------
    credit_payment = fields.Float('Credit Payment')
    credit_admin = fields.Float(' Credit Admin')
    credit_refund = fields.Float('Credit Refund')
    credit_wire = fields.Float('Credit Wire')
    credit_paypal = fields.Float('Credit Paypal')
    credit_bitcoin = fields.Float('Credit Bitcoin')
    admin_debit_tids = fields.Float('Admin Debit')

    total_amount = fields.Float('Total Amount:', compute='_compute_total_amount')
    total_credits = fields.Float('Total Credits', compute='_compute_total_credits')

    @api.one
    @api.depends('channel_groups_amount', 'local_numbers_amount', 'tollfree_numbers_amount', 'offnet_numbers_amount',
                 'international_numbers_amount', 'lnp_requests_amount', 'minutes_inbound_amount',
                 'minutes_outbound_amount', 'sipnav_minutes_outbound_amount', 'local_sms_in_amount',
                 'local_sms_out_amount', 'local_mms_in_amount', 'local_mms_out_amount', 'sc_sms_in_amount',
                 'sc_sms_out_amount', 'sc_mms_in_amount', 'sc_mms_out_amount', 'tf_sms_in_amount', 'tf_sms_out_amount',
                 'tf_mms_in_amount', 'tf_mms_out_amount', 'intl_sms_in_amount', 'intl_sms_out_amount',
                 'intl_mms_in_amount', 'intl_mms_out_amount', 'e911_amount')
    def _compute_total_amount(self):
        amounts_list = [self.channel_groups_amount, self.local_numbers_amount, self.tollfree_numbers_amount,
                        self.offnet_numbers_amount, self.international_numbers_amount, self.lnp_requests_amount,
                        self.minutes_inbound_amount, self.minutes_outbound_amount, self.sipnav_minutes_outbound_amount,
                        self.local_sms_in_amount, self.local_sms_out_amount, self.local_mms_in_amount,
                        self.local_mms_out_amount, self.sc_sms_in_amount, self.sc_sms_out_amount, self.sc_mms_in_amount,
                        self.sc_mms_out_amount, self.tf_sms_in_amount, self.tf_sms_out_amount, self.tf_mms_in_amount,
                        self.tf_mms_out_amount, self.intl_sms_in_amount, self.intl_sms_out_amount,
                        self.intl_mms_in_amount, self.intl_mms_out_amount, self.e911_amount]
        self.total_amount = sum(amounts_list)

    @api.one
    @api.depends('credit_payment', 'credit_admin', 'credit_refund', 'credit_wire', 'credit_paypal', 'credit_bitcoin')
    def _compute_total_credits(self):
        amounts_list = [self.credit_payment, self.credit_admin, self.credit_refund, self.credit_wire,
                        self.credit_paypal, self.credit_bitcoin]
        self.total_credits = sum(amounts_list)

    create_dt = fields.Datetime('Created')
    modify_dt = fields.Datetime('Modified')
