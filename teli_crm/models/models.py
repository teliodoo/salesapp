# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
# uncomment for debugging
# _logger.setLevel('DEBUG')

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    # Override fields we want to be required for account creation
    # contact_name = fields.Char('Contact Name', required=True)
    # email_from = fields.Char('Email', help="Email address of the contact", index=True, required=True)
    # partner_name = fields.Char("Customer Name", index=True, required=True,
        # help='The name of the future partner company that will be created while converting the lead into opportunity')
    # phone = fields.Char('Phone', required=True)

    username = fields.Char('Username', help='Provide the username you want to assign to the lead')
    account_credit = fields.Char('Initial Account Credit', default='25')

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
    def handle_partner_assignation(self, action='create', partner_id=False):
        # make call get data
        teliapi = self.env['teliapi.teliapi']
        current_user = self.env['res.users'].browse(self.user_id.id)

        if action == 'create':
            # customer doesn't exist
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
                self.message_post(content_subtype='plaintext', subject='Teli API Warning',
                    body='[WARNING] Encountered an issue attempting to create the new user.')
            else:
                self.message_post(content_subtype='plaintext', subject='Teli API Note',
                    body='[SUCCESS] New customer account was successfully created.')

        return super().handle_partner_assignation(action, partner_id)
