# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class teli_crm(models.Model):
    _inherit = 'crm.lead'

    def _format_phone_number(self, phone_number):
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

    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        _logger.warning(str(customer.__dict__))

        # make call get data
        teliapi = self.env['teliapi.teliapi']
        api_response = teliapi.get_user()
        #api_response = teliapi.create_user()

        # update the customer data and pass it on
        customer.write({
            'name': "%s %s" % (api_response['first_name'], api_response['last_name']),
            'email': api_response['email'],
            'phone': self._format_phone_number(api_response['phone_number'])
        })
        _logger.warning(str(customer.__dict__))

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
