# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel('DEBUG')

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    # Override fields we want to be required for account creation
    # contact_name = fields.Char('Contact Name', required=True)
    # email_from = fields.Char('Email', help="Email address of the contact", index=True, required=True)
    # partner_name = fields.Char("Customer Name", index=True, required=True,
        # help='The name of the future partner company that will be created while converting the lead into opportunity')
    # phone = fields.Char('Phone', required=True)

    # TODO Add a username field?
    # username =  fields.Char('Teli Username', required=True, help='Provide the username you want to assign to the lead')

    def _format_phone_number(self, phone_number):
        """ _format_phone_number - Attempts to print a phone number in a more
            readable format.
            @param phone_number
            @returns a pretty printed number
        """
        if len(phone_number) == 7:
            # format a 7 digit number
            return "%s-%s" % (phone_number[:3], phone_number[3:])
        elif len(phone_number) == 10:
            # format number with area code
            return "(%s) %s-%s" % (phone_number[:3], phone_number[3:6], phone_number[6:])
        elif len(phone_number) == 11:
            # format number with country and area code
            return "+%s (%s) %s-%s" % (phone_number[:1], phone_number[1:4], phone_number[4:7], phone_number[7:])

        # fail path
        return phone_number

    def _format_name(self, name):
        """ _format_name - takes the entire name param and attempts to parse it
            into only first and last names.  This assumes the number is formatted:
            first_name (middle_name or initial) last_name.
            @param name the value of the name field
            @returns first_name, last_name
        """
        name_array = name.split()

        if len(name_array) == 2:
            return name_array[0], name_array[1]
        else:
            first_name = ' '.join(name_array[:-1])
            last_name = name_array[-1]
            return first_name, last_name

    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        _logger.warning(str(customer.__dict__))

        # make call get data
        teliapi = self.env['teliapi.teliapi']
        _logger.debug("user_id is: %s" % self.user_id.id)
        # FIXME is this the correct way to get the lead2opportunity
        lead2opportunity = self.env['crm.lead2opportunity.partner'].search([('user_id', '=', self.user_id.id)], limit=1)

        _logger.debug("customer id is: %s" % customer)
        _logger.debug("opportunity action is: %s" % lead2opportunity.action)
        if lead2opportunity.action == 'create':
            # customer doesn't exist
            first_name, last_name = self._format_name(self.contact_name)
            # salesperson = self.env['res.users'].browse(self.user_id)
            params = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': self.phone,
                'email': self.email_from,
                'username': "%s.%s" % (first_name, last_name), # FIXME what should this be?
                'company_name': self.partner_name,
                # 'token': salesperson.sales_associate_token, # FIXME should come from res.users (lookup with crm.lead.user_id?)
            }
            create_response = teliapi.create_user(params)
            # TODO do we need to check the create_response to and buble up errors?

        return super()._convert_opportunity_data(customer, team_id)

    @api.multi
    def action_set_won(self):
        _logger.debug('landed in teli_crm.action_set_won')
        api_response = self.env['teliapi.teliapi'].get_user()

        return super().action_set_won()

    @api.multi
    def action_set_lost(self):
        _logger.debug('OH NO!!! lead has been lost!')
        return super().action_set_lost()
