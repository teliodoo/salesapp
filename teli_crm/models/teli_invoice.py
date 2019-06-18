# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')


class TeliInvoice(models.Model):
    _name = 'teli.invoice'

    _order = "create_dt DESC"

    def _calculate_rate(self, x, y):
        """
            _calculate_rate - simple method to calculate the per unit rate while
            defending against division by zero errors
        """
        try:
            return x / y
        except ZeroDivisionError:
            return 0

    crm_lead_id = fields.Many2one('crm.lead', string='Account', index=True)

    # Not used anymore but can't remove it because Odoo can't deal with changes...
    channel_groups_qty = fields.Integer('Channel Groups Quantity', default=0, invisible=1)

    # Channel Groups ----------------------------------------------------------------------
    channel_groups = fields.Integer('Channel Groups Quantity', default=0)
    channel_groups_price = fields.Float('Channel Groups Price', digits=(13, 2), default=0.0)
    channel_groups_rate = fields.Float('Channel Groups Rate', digits=(13, 6), compute='_compute_cg_rate')

    @api.one
    @api.depends('channel_groups', 'channel_groups_price')
    def _compute_cg_rate(self):
        self.channel_groups_rate = self._calculate_rate(self.channel_groups_price, self.channel_groups)

    # Local Numbers ----------------------------------------------------------------------
    local_numbers = fields.Integer('Local Numbers', default=0)
    local_numbers_price = fields.Float('Local Numbers Price', digits=(13, 2), default=0.0)
    local_numbers_rate = fields.Float('Local Numbers Rate', digits=(13, 6), compute='_compute_ln_rate')

    @api.one
    @api.depends('local_numbers', 'local_numbers_price')
    def _compute_ln_rate(self):
        self.local_numbers_rate = self._calculate_rate(self.local_numbers_price, self.local_numbers)

    # Tollfree Numbers ----------------------------------------------------------------------
    tollfree_numbers = fields.Integer('Tollfree Numbers', default=0)
    tollfree_numbers_price = fields.Float('Tollfree Numbers Price', digits=(13, 2), default=0.0)
    tollfree_numbers_rate = fields.Float('Tollfree Numbers Rate', digits=(13, 6), compute='_compute_tf_rate')

    @api.one
    @api.depends('tollfree_numbers', 'tollfree_numbers_price')
    def _compute_tf_rate(self):
        self.tollfree_numbers_rate = self._calculate_rate(self.tollfree_numbers_price, self.tollfree_numbers)

    # Offnet Numbers ----------------------------------------------------------------------
    offnet_numbers = fields.Integer('Offnet Numbers', default=0)
    offnet_numbers_price = fields.Float('Offnet Numbers Price', digits=(13, 2), default=0.0)
    offnet_numbers_rate = fields.Float('Offnet Numbers Rate', digits=(13, 6), compute='_compute_onn_rate')

    @api.one
    @api.depends('offnet_numbers', 'offnet_numbers_price')
    def _compute_onn_rate(self):
        self.offnet_numbers_rate = self._calculate_rate(self.offnet_numbers_price, self.offnet_numbers)

    # International Numbers ----------------------------------------------------------------------
    international_numbers = fields.Integer('International Numbers', default=0)
    international_numbers_price = fields.Float('International Numbers Price', digits=(13, 2), default=0.0)
    international_numbers_rate = fields.Float('International Numbers Rate', digits=(13, 6), compute='_compute_intl_rate')

    @api.one
    @api.depends('international_numbers', 'international_numbers_price')
    def _compute_intl_rate(self):
        self.international_numbers_rate = self._calculate_rate(self.international_numbers_price, self.international_numbers)

    # LNP Requests ----------------------------------------------------------------------
    # NOTE: not currently in invoice aggregate query
    lnp_requests = fields.Integer('LNP Requests', default=0)
    lnp_requests_price = fields.Float('LNP Requests Price', digits=(13, 2), default=0.0)
    lnp_requests_rate = fields.Float('LNP Requests Rate', digits=(13, 6), compute='_compute_lnp_rate')

    @api.one
    @api.depends('lnp_requests', 'lnp_requests_price')
    def _compute_lnp_rate(self):
        self.lnp_requests_rate = self._calculate_rate(self.lnp_requests_price, self.lnp_requests)

    # Minutes Inbound ----------------------------------------------------------------------
    minutes_inbound = fields.Integer('Minutes Inbound', default=0)
    minutes_inbound_price = fields.Float('Minutes Inbound Price', digits=(13, 2), default=0.0)
    minutes_inbound_rate = fields.Float('Minutes Inbound Rate', digits=(13, 6), compute='_compute_min_in_rate')

    @api.one
    @api.depends('minutes_inbound', 'minutes_inbound_price')
    def _compute_min_in_rate(self):
        self.minutes_inbound_rate = self._calculate_rate(self.minutes_inbound_price, self.minutes_inbound)

    # Minutes Outbound ----------------------------------------------------------------------
    minutes_outbound = fields.Integer('Minutes Outbound', default=0)
    minutes_outbound_price = fields.Float('Minutes Outbound Price', digits=(13, 2), default=0.0)
    minutes_outbound_rate = fields.Float('Minutes Outbound Rate', digits=(13, 6), compute='_compute_min_out_rate')

    @api.one
    @api.depends('minutes_outbound', 'minutes_outbound_price')
    def _compute_min_out_rate(self):
        self.minutes_outbound_rate = self._calculate_rate(self.minutes_outbound_price, self.minutes_outbound)

    # SIP/Nav Minutes Outbound ----------------------------------------------------------------------
    sipnav_minutes_outbound = fields.Integer('SIPNav Minutes Outbound', default=0)
    sipnav_minutes_outbound_price = fields.Float('SIPNav Minutes Outbound Price', digits=(13, 2), default=0.0)
    sipnav_minutes_outbound_rate = fields.Float('SIPNav Minutes Outbound Rate', digits=(13, 6), compute='_compute_sipnav_rate')

    @api.one
    @api.depends('sipnav_minutes_outbound', 'sipnav_minutes_outbound_price')
    def _compute_sipnav_rate(self):
        self.sipnav_minutes_outbound_rate = self._calculate_rate(self.sipnav_minutes_outbound_price, self.sipnav_minutes_outbound)

    # Local SMS Inbound ----------------------------------------------------------------------
    local_sms_in = fields.Integer('Local SMS Inbound', default=0)
    local_sms_in_price = fields.Float('Local SMS Inbound Price', digits=(13, 2), default=0.0)
    local_sms_in_rate = fields.Float('Local SMS Inbound Rate', digits=(13, 6), compute='_compute_local_sms_in_rate')

    @api.one
    @api.depends('local_sms_in', 'local_sms_in_price')
    def _compute_local_sms_in_rate(self):
        self.local_sms_in_rate = self._calculate_rate(self.local_sms_in_price, self.local_sms_in)

    # Local SMS Outbound ----------------------------------------------------------------------
    local_sms_out = fields.Integer('Local SMS Outbound', default=0)
    local_sms_out_price = fields.Float('Local SMS Outbound Price', digits=(13, 2), default=0.0)
    local_sms_out_rate = fields.Float('Local SMS Outbound Rate', digits=(13, 6), compute='_compute_local_sms_out_rate')

    @api.one
    @api.depends('local_sms_out', 'local_sms_out_price')
    def _compute_local_sms_out_rate(self):
        self.local_sms_out_rate = self._calculate_rate(self.local_sms_out_price, self.local_sms_out)

    # Local MMS Inbound ----------------------------------------------------------------------
    local_mms_in = fields.Integer('Local MMS Inbound', default=0)
    local_mms_in_price = fields.Float('Local MMS Inbound Price', digits=(13, 2), default=0.0)
    local_mms_in_rate = fields.Float('Local MMS Inbound Rate', digits=(13, 6), compute='_compute_local_mms_in_rate')

    @api.one
    @api.depends('local_mms_in', 'local_mms_in_price')
    def _compute_local_mms_in_rate(self):
        self.local_mms_in_rate = self._calculate_rate(self.local_mms_in_price, self.local_mms_in)

    # Local MMS Outbound ----------------------------------------------------------------------
    local_mms_out = fields.Integer('Local MMS Outbound', default=0)
    local_mms_out_price = fields.Float('Local MMS Outbound Price', digits=(13, 2), default=0.0)
    local_mms_out_rate = fields.Float('Local MMS Outbound Rate', digits=(13, 6), compute='_compute_local_mms_out_rate')

    @api.one
    @api.depends('local_mms_out', 'local_mms_out_price')
    def _compute_local_mms_out_rate(self):
        self.local_mms_out_rate = self._calculate_rate(self.local_mms_out_price, self.local_mms_out)

    # Shortcode SMS Inbound ----------------------------------------------------------------------
    sc_sms_in = fields.Integer('Shortcode SMS Inbound', default=0)
    sc_sms_in_price = fields.Float('Shortcode SMS Inbound Price', digits=(13, 2), default=0.0)
    sc_sms_in_rate = fields.Float('Shortcode SMS Inbound Rate', digits=(13, 6), compute='_compute_sc_sms_in_rate')

    @api.one
    @api.depends('sc_sms_in', 'sc_sms_in_price')
    def _compute_sc_sms_in_rate(self):
        self.sc_sms_in_rate = self._calculate_rate(self.sc_sms_in_price, self.sc_sms_in)

    # Shortcode SMS Outbound ----------------------------------------------------------------------
    sc_sms_out = fields.Integer('Shortcode SMS Outbound', default=0)
    sc_sms_out_price = fields.Float('Shortcode SMS Outbound Price', digits=(13, 2), default=0.0)
    sc_sms_out_rate = fields.Float('Shortcode SMS Outbound Rate', digits=(13, 6), compute='_compute_sc_sms_out_rate')

    @api.one
    @api.depends('sc_sms_out', 'sc_sms_out_price')
    def _compute_sc_sms_out_rate(self):
        self.sc_sms_out_rate = self._calculate_rate(self.sc_sms_out_price, self.sc_sms_out)

    # Shortcode MMS Inbound ----------------------------------------------------------------------
    sc_mms_in = fields.Integer('Shortcode MMS Inbound', default=0)
    sc_mms_in_price = fields.Float('Shortcode MMS Inbound Price', digits=(13, 2), default=0.0)
    sc_mms_in_rate = fields.Float('Shortcode MMS Inbound Rate', digits=(13, 6), compute='_compute_sc_mms_in_rate')

    @api.one
    @api.depends('sc_mms_in', 'sc_mms_in_price')
    def _compute_sc_mms_in_rate(self):
        self.sc_mms_in_rate = self._calculate_rate(self.sc_mms_in_price, self.sc_mms_in)

    # Shortcode MMS Outbound ----------------------------------------------------------------------
    sc_mms_out = fields.Integer('Shortcode MMS Outbound', default=0)
    sc_mms_out_price = fields.Float('Shortcode MMS Outbound Price', digits=(13, 2), default=0.0)
    sc_mms_out_rate = fields.Float('Shortcode MMS Outbound Rate', digits=(13, 6), compute='_compute_sc_mms_out_rate')

    @api.one
    @api.depends('sc_mms_out', 'sc_mms_out_price')
    def _compute_sc_mms_out_rate(self):
        self.sc_mms_out_rate = self._calculate_rate(self.sc_mms_out_price, self.sc_mms_out)

    # Tollfree SMS Inbound ----------------------------------------------------------------------
    tf_sms_in = fields.Integer('Tollfree SMS Inbound', default=0)
    tf_sms_in_price = fields.Float('Tollfree SMS Inbound Price', digits=(13, 2), default=0.0)
    tf_sms_in_rate = fields.Float('Tollfree SMS Inbound Rate', digits=(13, 6), compute='_compute_tf_sms_in_rate')

    @api.one
    @api.depends('tf_sms_in', 'tf_sms_in_price')
    def _compute_tf_sms_in_rate(self):
        self.tf_sms_in_rate = self._calculate_rate(self.tf_sms_in_price, self.tf_sms_in)

    # Tollfree SMS Outbound ----------------------------------------------------------------------
    tf_sms_out = fields.Integer('Tollfree SMS Outbound', default=0)
    tf_sms_out_price = fields.Float('Tollfree SMS Outbound Price', digits=(13, 2), default=0.0)
    tf_sms_out_rate = fields.Float('Tollfree SMS Outbound Rate', digits=(13, 6), compute='_compute_tf_sms_out_rate')

    @api.one
    @api.depends('tf_sms_out', 'tf_sms_out_price')
    def _compute_tf_sms_out_rate(self):
        self.tf_sms_out_rate = self._calculate_rate(self.tf_sms_out_price, self.tf_sms_out)

    # Tollfree MMS Inbound ----------------------------------------------------------------------
    tf_mms_in = fields.Integer('Tollfree MMS Inbound', default=0)
    tf_mms_in_price = fields.Float('Tollfree MMS Inbound Price', digits=(13, 2), default=0.0)
    tf_mms_in_rate = fields.Float('Tollfree MMS Inbound Rate', digits=(13, 6), compute='_compute_tf_mms_in_rate')

    @api.one
    @api.depends('tf_mms_in', 'tf_mms_in_price')
    def _compute_tf_mms_in_rate(self):
        self.tf_mms_in_rate = self._calculate_rate(self.tf_mms_in_price, self.tf_mms_in)

    # Tollfree MMS Outbound ----------------------------------------------------------------------
    tf_mms_out = fields.Integer('Tollfree MMS Outbound', default=0)
    tf_mms_out_price = fields.Float('Tollfree MMS Outbound Price', digits=(13, 2), default=0.0)
    tf_mms_out_rate = fields.Float('Tollfree MMS Outbound Rate', digits=(13, 6), compute='_compute_tf_mms_out_rate')

    @api.one
    @api.depends('tf_mms_out', 'tf_mms_out_price')
    def _compute_tf_mms_out_rate(self):
        self.tf_mms_out_rate = self._calculate_rate(self.tf_mms_out_price, self.tf_mms_out)

    # International SMS Inbound ----------------------------------------------------------------------
    intl_sms_in = fields.Integer('International SMS Inbound', default=0)
    intl_sms_in_price = fields.Float('International SMS Inbound Price', digits=(13, 2), default=0.0)
    intl_sms_in_rate = fields.Float('International SMS Inbound Rate', digits=(13, 6), compute='_compute_intl_sms_in_rate')

    @api.one
    @api.depends('intl_sms_in', 'intl_sms_in_price')
    def _compute_intl_sms_in_rate(self):
        self.intl_sms_in_rate = self._calculate_rate(self.intl_sms_in_price, self.intl_sms_in)

    # International SMS Outbound ----------------------------------------------------------------------
    intl_sms_out = fields.Integer('International SMS Outbound', default=0)
    intl_sms_out_price = fields.Float('International SMS Outbound Price', digits=(13, 2), default=0.0)
    intl_sms_out_rate = fields.Float('International SMS Outbound Rate', digits=(13, 6), compute='_compute_intl_sms_out_rate')

    @api.one
    @api.depends('intl_sms_out', 'intl_sms_out_price')
    def _compute_intl_sms_out_rate(self):
        self.intl_sms_out_rate = self._calculate_rate(self.intl_sms_out_price, self.intl_sms_out)

    # International MMS Inbound ----------------------------------------------------------------------
    intl_mms_in = fields.Integer('International MMS Inbound', default=0)
    intl_mms_in_price = fields.Float('International MMS Inbound Price', digits=(13, 2), default=0.0)
    intl_mms_in_rate = fields.Float('International MMS Inbound Rate', digits=(13, 6), compute='_compute_intl_mms_in_rate')

    @api.one
    @api.depends('intl_mms_in', 'intl_mms_in_price')
    def _compute_intl_mms_in_rate(self):
        self.intl_mms_in_rate = self._calculate_rate(self.intl_mms_in_price, self.intl_mms_in)

    # International MMS Outbound ----------------------------------------------------------------------
    intl_mms_out = fields.Integer('International MMS Outbound', default=0)
    intl_mms_out_price = fields.Float('International MMS Outbound Price', digits=(13, 2), default=0.0)
    intl_mms_out_rate = fields.Float('International MMS Outbound Rate', digits=(13, 6), compute='_compute_intl_mms_out_rate')

    @api.one
    @api.depends('intl_mms_out', 'intl_mms_out_price')
    def _compute_intl_mms_out_rate(self):
        self.intl_mms_out_rate = self._calculate_rate(self.intl_mms_out_price, self.intl_mms_out)

    # SMM SMS Inbound ---------------------------------------------------------------------------------
    smm_sms_in = fields.Integer('SMM Inbound', default=0)
    smm_sms_in_price = fields.Float('SMM Inbound Price', digits=(13, 2), default=0.0)
    smm_sms_in_rate = fields.Float('SMM Inbound Rate', digits=(13, 6), compute='_compute_smm_sms_in_rate')

    @api.one
    @api.depends('smm_sms_in', 'smm_sms_in_price')
    def _compute_smm_sms_in_rate(self):
        self.smm_sms_in_rate = self._calculate_rate(self.smm_sms_in_price, self.smm_sms_in)

    # SMM SMS Outbound --------------------------------------------------------------------------------
    smm_sms_out = fields.Integer('SMM Inbound', default=0)
    smm_sms_out_price = fields.Float('SMM Inbound Price', digits=(13, 2), default=0.0)
    smm_sms_out_rate = fields.Float('SMM Inbound Rate', digits=(13, 6), compute='_compute_smm_sms_out_rate')

    @api.one
    @api.depends('smm_sms_out', 'smm_sms_out_price')
    def _compute_smm_sms_out_rate(self):
        self.smm_sms_out_rate = self._calculate_rate(self.smm_sms_out_price, self.smm_sms_out)

    # Emergency 911 Service ----------------------------------------------------------------------
    e911 = fields.Integer('911 Service', default=0)
    e911_price = fields.Float('911 Service Price', digits=(13, 2), default=0.0)
    e911_rate = fields.Float('911 Service Rate', digits=(13, 6), compute='_compute_e911_rate')

    @api.one
    @api.depends('e911', 'e911_price')
    def _compute_e911_rate(self):
        self.e911_rate = self._calculate_rate(self.e911_price, self.e911)

    # ------------------------------------------------------------------------- [voice_did_tf_in]
    voice_did_tf_in = fields.Integer('Voice Tollfree In', default=0)
    voice_did_tf_in_price = fields.Float('Voice Tollfree In Price', digits=(13, 2), default=0.0)
    voice_did_tf_in_rate = fields.Float('Voice Tollfree In Rate', digits=(13, 6), compute='_compute_voice_did_tf_in')

    @api.one
    @api.depends('voice_did_tf_in', 'voice_did_tf_in_price')
    def _compute_voice_did_tf_in(self):
        self.voice_did_tf_in_rate = self._calculate_rate(self.voice_did_tf_in_price, self.voice_did_tf_in)

    # ------------------------------------------------------------------------- [voice_did_local_in]
    voice_did_local_in = fields.Integer('Voice Local In', default=0)
    voice_did_local_in_price = fields.Float('Voice Local In Price', digits=(13, 2), default=0.0)
    voice_did_local_in_rate = fields.Float('Voice Local In Rate', digits=(13, 6), compute='_compute_voice_did_local_in')

    @api.one
    @api.depends('voice_did_local_in', 'voice_did_local_in_price')
    def _compute_voice_did_local_in(self):
        self.voice_did_local_in_rate = self._calculate_rate(self.voice_did_local_in_price, self.voice_did_local_in)

    # ------------------------------------------------------------------------- [voice_did_intl_in]
    voice_did_intl_in = fields.Integer('Voice International In', default=0)
    voice_did_intl_in_price = fields.Float('Voice International In Price', digits=(13, 2), default=0.0)
    voice_did_intl_in_rate = fields.Float('Voice International In Rate', digits=(13, 6),
                                          compute='_compute_voice_did_intl_in')

    @api.one
    @api.depends('voice_did_intl_in', 'voice_did_intl_in_price')
    def _compute_voice_did_intl_in(self):
        self.voice_did_intl_in_rate = self._calculate_rate(self.voice_did_intl_in_price, self.voice_did_intl_in)

    # ------------------------------------------------------------------------- [voice_term_usa_out]
    voice_term_usa_out = fields.Integer('Voice Term USA Out', default=0)
    voice_term_usa_out_price = fields.Float('Voice Term USA Out Price', digits=(13, 2), default=0.0)
    voice_term_usa_out_rate = fields.Float('Voice Term USA Out Rate', digits=(13, 6),
                                           compute='_compute_voice_term_usa_out')

    @api.one
    @api.depends('voice_term_usa_out', 'voice_term_usa_out_price')
    def _compute_voice_term_usa_out(self):
        self.voice_term_usa_out_rate = self._calculate_rate(self.voice_term_usa_out_price, self.voice_term_usa_out)

    # ------------------------------------------------------------------------- [voice_term_intl_out]
    voice_term_intl_out = fields.Integer('Voice Term International Out', default=0)
    voice_term_intl_out_price = fields.Float('Voice Term International Out Price', digits=(13, 2), default=0.0)
    voice_term_intl_out_rate = fields.Float('Voice Term International Out Rate', digits=(13, 6),
                                            compute='_compute_voice_term_intl_out')

    @api.one
    @api.depends('voice_term_intl_out', 'voice_term_intl_out_price')
    def _compute_voice_term_intl_out(self):
        self.voice_term_intl_out_rate = self._calculate_rate(self.voice_term_intl_out_price, self.voice_term_intl_out)

    # ------------------------------------------------------------------------- [voice_term_tf_out]
    voice_term_tf_out = fields.Integer('Voice Term Tollfree Out', default=0)
    voice_term_tf_out_price = fields.Float('Voice Term Tollfree Out Price', digits=(13, 2), default=0.0)
    voice_term_tf_out_rate = fields.Float('Voice Term Tollfree Out Rate', digits=(13, 6),
                                          compute='_compute_voice_term_tf_out')

    @api.one
    @api.depends('voice_term_tf_out', 'voice_term_tf_out_price')
    def _compute_voice_term_tf_out(self):
        self.voice_term_tf_out_rate = self._calculate_rate(self.voice_term_tf_out_price, self.voice_term_tf_out)

    # ------------------------------------------------------------------------- [voice_term_fax_out]
    voice_term_fax_out = fields.Integer('Voice Term Fax Out', default=0)
    voice_term_fax_out_price = fields.Float('Voice Term Fax Out Price', digits=(13, 2), default=0.0)
    voice_term_fax_out_rate = fields.Float('Voice Term Fax Out Rate', digits=(13, 6),
                                           compute='_compute_voice_term_fax_out')

    @api.one
    @api.depends('voice_term_fax_out', 'voice_term_fax_out_price')
    def _compute_voice_term_fax_out(self):
        self.voice_term_fax_out_rate = self._calculate_rate(self.voice_term_fax_out_price, self.voice_term_fax_out)

    # NOTE: These are additional types found in teli_cust_agg, but don't appear to be used... yet?
    # billing_dids_tf
    # billing_dids_intl
    # billing_dids_local
    # billing_dids_e911
    # billing_dids_offnet
    # billing_dids_channelgroups
    # billing_dids_shortcode
    # billing_dids_nrc
    # billing_dids_porting
    # billing_dids_vanity
    # billing-services-hosting
    # billing-services-other
    # billing-dids-total-monthly
    # billing-services-total-monthly

    # ------------------------------------------------------------------------- [billing_cnam_query]
    billing_cnam_query = fields.Integer('Billing CNAM Query', default=0)
    billing_cnam_query_price = fields.Float('Billing CNAM Query Price', digits=(13, 2), default=0.0)
    billing_cnam_query_rate = fields.Float('Billing CNAM Query Rate', digits=(13, 6),
                                           compute='_compute_billing_cnam_query')

    @api.one
    @api.depends('billing_cnam_query', 'billing_cnam_query_price')
    def _compute_billing_cnam_query(self):
        self.billing_cnam_query_rate = self._calculate_rate(self.billing_cnam_query_price, self.billing_cnam_query)

    # ------------------------------------------------------------------------- [billing_lrn_query]
    billing_lrn_query = fields.Integer('Billing LRN Query', default=0)
    billing_lrn_query_price = fields.Float('Billing LRN Query Price', digits=(13, 2), default=0.0)
    billing_lrn_query_rate = fields.Float('Billing LRN Query Rate', digits=(13, 6),
                                          compute='_compute_billing_lrn_query')

    @api.one
    @api.depends('billing_lrn_query', 'billing_lrn_query_price')
    def _compute_billing_lrn_query(self):
        self.billing_lrn_query_rate = self._calculate_rate(self.billing_lrn_query_price, self.billing_lrn_query)

    # Summary Information -----------------------------------------------------------------------
    credit_payment = fields.Float('Credit Payment')
    credit_admin = fields.Float(' Credit Admin')
    credit_refund = fields.Float('Credit Refund')
    credit_wire = fields.Float('Credit Wire')
    credit_paypal = fields.Float('Credit Paypal')
    credit_bitcoin = fields.Float('Credit Bitcoin')
    display_adt = fields.Boolean('Display Admin Debits TransactionIds?', default=False, compute='_compute_display_adt')
    adjustment_total = fields.Float('Transaction Totals', digits=(13, 2), default=0.0, readonly=True)
    admin_debit_tids = fields.Html('Other Charges', readonly=True, default="SKIPME")

    @api.one
    @api.depends('admin_debit_tids')
    def _compute_display_adt(self):
        _logger.debug("value of admin_debit_tids is: " + self.admin_debit_tids)
        if "SKIPME" in self.admin_debit_tids:
            self.display_adt = False
        else:
            self.display_adt = True

    total_price = fields.Float('Total Amount:', compute='_compute_total_price')
    total_credits = fields.Float('Total Credits', compute='_compute_total_credits')

    @api.one
    @api.depends('channel_groups_price', 'local_numbers_price', 'tollfree_numbers_price', 'offnet_numbers_price',
                 'international_numbers_price', 'lnp_requests_price', 'minutes_inbound_price',
                 'minutes_outbound_price', 'sipnav_minutes_outbound_price', 'local_sms_in_price',
                 'local_sms_out_price', 'local_mms_in_price', 'local_mms_out_price', 'sc_sms_in_price',
                 'sc_sms_out_price', 'sc_mms_in_price', 'sc_mms_out_price', 'tf_sms_in_price', 'tf_sms_out_price',
                 'tf_mms_in_price', 'tf_mms_out_price', 'intl_sms_in_price', 'intl_sms_out_price',
                 'intl_mms_in_price', 'intl_mms_out_price', 'smm_sms_in_price', 'smm_sms_out_price', 'e911_price',
                 'voice_did_tf_in_price', 'voice_did_intl_in_price', 'voice_did_local_in_price',
                 'voice_term_usa_out_price', 'voice_term_intl_out_price', 'voice_term_tf_out_price',
                 'voice_term_fax_out_price', 'billing_lrn_query_price', 'billing_cnam_query_price', 'adjustment_total')
    def _compute_total_price(self):
        amounts_list = [self.channel_groups_price, self.local_numbers_price, self.tollfree_numbers_price,
                        self.offnet_numbers_price, self.international_numbers_price, self.lnp_requests_price,
                        self.minutes_inbound_price, self.minutes_outbound_price, self.sipnav_minutes_outbound_price,
                        self.local_sms_in_price, self.local_sms_out_price, self.local_mms_in_price,
                        self.local_mms_out_price, self.sc_sms_in_price, self.sc_sms_out_price, self.sc_mms_in_price,
                        self.sc_mms_out_price, self.tf_sms_in_price, self.tf_sms_out_price, self.tf_mms_in_price,
                        self.tf_mms_out_price, self.intl_sms_in_price, self.intl_sms_out_price,
                        self.intl_mms_in_price, self.intl_mms_out_price, self.smm_sms_in_price, self.smm_sms_out_price,
                        self.e911_price, self.voice_did_tf_in_price, self.voice_did_intl_in_price,
                        self.voice_did_local_in_price, self.voice_term_usa_out_price, self.voice_term_intl_out_price,
                        self.voice_term_tf_out_price, self.voice_term_fax_out_price, self.billing_lrn_query_price,
                        self.billing_cnam_query_price, self.adjustment_total]
        self.total_price = sum(amounts_list)

    @api.one
    @api.depends('credit_payment', 'credit_admin', 'credit_refund', 'credit_wire', 'credit_paypal', 'credit_bitcoin')
    def _compute_total_credits(self):
        amounts_list = [self.credit_payment, self.credit_admin, self.credit_refund, self.credit_wire,
                        self.credit_paypal, self.credit_bitcoin]
        self.total_credits = sum(amounts_list)

    create_dt = fields.Datetime('Date Created')
    modify_dt = fields.Datetime('Last Modified')
