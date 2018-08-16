# -*- coding: utf-8 -*-
from odoo import http

# class TeliCrm(http.Controller):
#     @http.route('/teli_crm/teli_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/teli_crm/teli_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('teli_crm.listing', {
#             'root': '/teli_crm/teli_crm',
#             'objects': http.request.env['teli_crm.teli_crm'].search([]),
#         })

#     @http.route('/teli_crm/teli_crm/objects/<model("teli_crm.teli_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('teli_crm.object', {
#             'object': obj
#         })